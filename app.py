import os
import sys
import logging
import urllib.request
import traceback
from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta
import secrets
import numpy as np

# Configure logging to output to console immediately
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

print("\n" + "="*50)
print("🚀 FLASK APP STARTING UP")
print("="*50 + "\n")
sys.stdout.flush()

# Try to import utils with error handling
try:
    from utils.model_loader import load_model_and_scaler, DummyScaler
    from utils.feature_extractor import extract_features, get_feature_names
    print("✅ Utils imported successfully")
    sys.stdout.flush()
except Exception as e:
    print(f"❌ Failed to import utils: {str(e)}")
    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
    raise

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(minutes=30)

# Model download function
def download_model_if_missing():
    """Download model from GitHub if not present"""
    model_path = "phishing_model.pkl"
    github_url = "https://github.com/Ayush-Kumar-45/Phishing-URL-Detection/raw/master/phishing_model.pkl"
    
    if not os.path.exists(model_path):
        print(f"📥 Model not found locally. Downloading from GitHub...")
        sys.stdout.flush()
        try:
            urllib.request.urlretrieve(github_url, model_path)
            file_size = os.path.getsize(model_path)
            print(f"✅ Model downloaded successfully! Size: {file_size} bytes")
            sys.stdout.flush()
            return True
        except Exception as e:
            print(f"❌ Failed to download model: {str(e)}")
            sys.stdout.flush()
            return False
    else:
        file_size = os.path.getsize(model_path)
        print(f"✅ Model found locally. Size: {file_size} bytes")
        sys.stdout.flush()
        return True

# Download model if missing
download_model_if_missing()

# Load model and scaler at startup
try:
    print("🔄 Attempting to load model and scaler...")
    sys.stdout.flush()
    MODEL, SCALER = load_model_and_scaler()
    print("✅ Model and scaler loaded successfully!")
    sys.stdout.flush()
    
    # Verify feature count
    if hasattr(MODEL, 'n_features_in_'):
        expected_features = MODEL.n_features_in_
        print(f"📊 Model expects {expected_features} features")
        if expected_features != 23:
            print(f"⚠️ Warning: Model expects {expected_features} features, but code uses 23")
        sys.stdout.flush()
    else:
        print("ℹ️ Model doesn't expose n_features_in_, assuming it expects 23 features")
        sys.stdout.flush()
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to load model: {str(e)}")
    traceback.print_exc(file=sys.stdout)
    sys.stdout.flush()
    MODEL = None
    SCALER = None

print("="*50 + "\n")
sys.stdout.flush()

# Debug endpoint - place this at the VERY TOP of routes
@app.route('/debug-direct')
def debug_direct():
    """Direct debug endpoint that doesn't require model loading"""
    import os
    import sys
    
    result = {
        'status': 'Debug endpoint working',
        'cwd': os.getcwd(),
        'files_in_cwd': os.listdir('.'),
        'python_version': sys.version,
        'model_loaded': MODEL is not None,
    }
    
    # Check for model file in various locations
    model_paths = [
        '/app/phishing_model.pkl',
        './phishing_model.pkl',
        'phishing_model.pkl',
        '../phishing_model.pkl',
    ]
    
    for path in model_paths:
        result[f'model_exists_{path}'] = os.path.exists(path)
        if os.path.exists(path):
            result[f'model_size_{path}'] = os.path.getsize(path)
    
    # Check for .pkl files anywhere
    pkl_files = []
    for root, dirs, files in os.walk('/app'):
        for file in files:
            if file.endswith('.pkl'):
                pkl_files.append(os.path.join(root, file))
    result['all_pkl_files'] = pkl_files
    
    return jsonify(result)

@app.route('/debug-paths')
def debug_paths():
    """Debug endpoint to check file paths"""
    import os
    import sys
    
    result = {
        'current_working_dir': os.getcwd(),
        'python_path': sys.path,
        'files_in_current_dir': os.listdir('.'),
        'model_exists': os.path.exists('phishing_model.pkl'),
        'model_absolute_path': os.path.abspath('phishing_model.pkl') if os.path.exists('phishing_model.pkl') else 'Not found',
        'model_size': os.path.getsize('phishing_model.pkl') if os.path.exists('phishing_model.pkl') else 0,
        'utils_exists': os.path.exists('utils'),
        'utils_files': os.listdir('utils') if os.path.exists('utils') else [],
    }
    return jsonify(result)

@app.route('/debug-files')
def debug_files():
    """Comprehensive file debugging"""
    import os
    import subprocess
    
    result = {
        'current_dir': os.getcwd(),
        'current_dir_files': os.listdir('.'),
        'app_dir_files': os.listdir('/app') if os.path.exists('/app') else [],
    }
    
    # Search for .pkl files
    pkl_files = []
    for root, dirs, files in os.walk('/app'):
        for file in files:
            if file.endswith('.pkl') or file.endswith('.pkl.gz'):
                full_path = os.path.join(root, file)
                pkl_files.append({
                    'path': full_path,
                    'size': os.path.getsize(full_path),
                    'exists': os.path.exists(full_path)
                })
    
    result['pkl_files'] = pkl_files
    
    # Try to get disk usage
    try:
        result['disk_usage'] = subprocess.check_output(['df', '-h']).decode('utf-8')
    except:
        pass
    
    return jsonify(result)

@app.route('/debug-download')
def debug_download():
    """Try to download model from GitHub"""
    import urllib.request
    import os
    
    github_url = "https://github.com/Ayush-Kumar-45/Phishing-URL-Detection/raw/master/phishing_model.pkl"
    local_path = "/app/phishing_model_downloaded.pkl"
    
    try:
        urllib.request.urlretrieve(github_url, local_path)
        return jsonify({
            'success': True,
            'message': 'Model downloaded successfully',
            'size': os.path.getsize(local_path),
            'path': local_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    if MODEL is None:
        return jsonify({
            'status': 'degraded',
            'message': 'Model not loaded',
            'model_loaded': False
        }), 503
    
    expected_features = MODEL.n_features_in_ if hasattr(MODEL, 'n_features_in_') else 'unknown'
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'model_type': type(MODEL).__name__,
        'scaler_loaded': SCALER is not None and not isinstance(SCALER, DummyScaler),
        'expected_features': expected_features,
        'features_provided': 23
    })

@app.route('/')
def index():
    """Home page"""
    if MODEL is None:
        return render_template('error.html', 
                             error="Model not loaded. Please check the logs.",
                             details="The machine learning model could not be loaded.")
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict if a URL is phishing or legitimate"""
    try:
        # Check if model is loaded
        if MODEL is None:
            return render_template('result.html', 
                                 error="System is not ready. Please try again later.",
                                 url=request.form.get('url', ''))
        
        # Get URL from form
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template('result.html', 
                                 error="Please enter a URL",
                                 url=url)
        
        # Add http:// if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Log the prediction request
        logging.info(f"Predicting URL: {url}")
        
        # Extract features from URL
        features = extract_features(url)
        
        # Get feature names in correct order
        feature_names = get_feature_names()
        
        # Create feature array in correct order
        feature_values = [features.get(name, 0) for name in feature_names]
        feature_array = np.array([feature_values])
        
        logging.info(f"Feature array shape: {feature_array.shape}")
        logging.info(f"First 5 feature values: {feature_values[:5]}")
        
        # Scale features (if scaler is available, otherwise use as is)
        if SCALER is not None and not isinstance(SCALER, DummyScaler):
            features_scaled = SCALER.transform(feature_array)
        else:
            features_scaled = feature_array
        
        # Make prediction
        if hasattr(MODEL, 'predict_proba'):
            prediction = MODEL.predict(features_scaled)[0]
            probabilities = MODEL.predict_proba(features_scaled)[0]
            
            if prediction == 1:
                confidence = float(probabilities[1] * 100)
            else:
                confidence = float(probabilities[0] * 100)
        else:
            # For models without predict_proba
            prediction = MODEL.predict(features_scaled)[0]
            confidence = 95.0  # Default confidence
        
        # Interpret result
        if prediction == 1:
            result = "phishing"
            message = "⚠️ WARNING: This URL appears to be a PHISHING website!"
            alert_class = "alert-danger"
            icon = "fa-exclamation-triangle"
        else:
            result = "legitimate"
            message = "✅ SAFE: This URL appears to be LEGITIMATE"
            alert_class = "alert-success"
            icon = "fa-check-circle"
        
        # Log prediction result
        logging.info(f"Prediction for {url}: {result} (confidence: {confidence:.2f}%)")
        
        # Store in session for history
        if 'history' not in session:
            session['history'] = []
        
        session['history'].append({
            'url': url[:50] + '...' if len(url) > 50 else url,
            'result': result,
            'confidence': f"{confidence:.2f}%"
        })
        session.modified = True
        
        return render_template('result.html',
                             url=url,
                             result=result,
                             confidence=f"{confidence:.2f}",
                             message=message,
                             alert_class=alert_class,
                             icon=icon,
                             features=features)
    
    except Exception as e:
        logging.error(f"Error predicting URL: {str(e)}")
        logging.error(traceback.format_exc())
        return render_template('result.html',
                             error=f"An error occurred: {str(e)}",
                             url=url if 'url' in locals() else '')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        if MODEL is None:
            return jsonify({'error': 'Model not loaded'}), 503
        
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Add http:// if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Extract features
        features = extract_features(url)
        feature_names = get_feature_names()
        feature_values = [features.get(name, 0) for name in feature_names]
        feature_array = np.array([feature_values])
        
        if SCALER is not None and not isinstance(SCALER, DummyScaler):
            features_scaled = SCALER.transform(feature_array)
        else:
            features_scaled = feature_array
            
        prediction = MODEL.predict(features_scaled)[0]
        
        if hasattr(MODEL, 'predict_proba'):
            probabilities = MODEL.predict_proba(features_scaled)[0]
            confidence = float(probabilities[1] if prediction == 1 else probabilities[0])
        else:
            confidence = 0.95
        
        return jsonify({
            'success': True,
            'url': url,
            'prediction': 'phishing' if prediction == 1 else 'legitimate',
            'confidence': confidence,
            'features': {name: features.get(name, 0) for name in feature_names[:10]}
        })
    
    except Exception as e:
        logging.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """View prediction history"""
    history_list = session.get('history', [])
    return render_template('history.html', history=history_list)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear prediction history"""
    session.pop('history', None)
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server Error: {error}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
