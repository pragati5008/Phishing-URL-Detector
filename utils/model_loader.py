import pickle
import os
import sys
import gzip
import logging

def find_model_file():
    """Search for model file in all possible locations"""
    possible_paths = [
        '/app/phishing_model.pkl',
        '/app/phishing_model.pkl.gz',
        '/app/model/phishing_model.pkl',
        '/app/src/phishing_model.pkl',
        './phishing_model.pkl',
        '../phishing_model.pkl',
        'phishing_model.pkl',
        '/opt/render/project/src/phishing_model.pkl',
        '/opt/render/project/src/phishing_model.pkl.gz',
    ]
    
    print("\n=== SEARCHING FOR MODEL FILE ===")
    sys.stdout.flush()
    
    for path in possible_paths:
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            print(f"✓ FOUND: {path} (Size: {file_size} bytes)")
            sys.stdout.flush()
            return path
    
    # If not found in common paths, search entire /app directory
    print("\nSearching entire /app directory...")
    sys.stdout.flush()
    
    for root, dirs, files in os.walk('/app'):
        for file in files:
            if file.endswith('.pkl') or file.endswith('.pkl.gz'):
                full_path = os.path.join(root, file)
                file_size = os.path.getsize(full_path)
                print(f"✓ FOUND: {full_path} (Size: {file_size} bytes)")
                sys.stdout.flush()
                return full_path
    
    return None

def load_model_and_scaler():
    """
    Load the trained phishing detection model with robust path searching
    """
    try:
        # Print debug info
        print("\n" + "="*50)
        print("MODEL LOADING DEBUG")
        print("="*50)
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python version: {sys.version}")
        print(f"Files in current directory: {os.listdir('.')}")
        sys.stdout.flush()
        
        # Find model file
        model_path = find_model_file()
        
        if model_path is None:
            error_msg = "Could not find phishing_model.pkl anywhere in the container"
            print(f"❌ {error_msg}")
            sys.stdout.flush()
            raise FileNotFoundError(error_msg)
        
        # Load model (handle compressed files)
        print(f"\nLoading model from: {model_path}")
        sys.stdout.flush()
        
        if model_path.endswith('.gz'):
            with gzip.open(model_path, 'rb') as f:
                model = pickle.load(f)
        else:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        
        print(f"✓ Model loaded successfully!")
        print(f"  Type: {type(model).__name__}")
        sys.stdout.flush()
        
        # Get model features
        if hasattr(model, 'n_features_in_'):
            print(f"  Features expected: {model.n_features_in_}")
        elif hasattr(model, 'n_features_'):
            print(f"  Features expected: {model.n_features_}")
        sys.stdout.flush()
        
        # Try to load scaler
        scaler_path = '/app/scaler.pkl'
        if os.path.exists(scaler_path) and os.path.getsize(scaler_path) > 0:
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            print("✓ Scaler loaded successfully")
        else:
            scaler = DummyScaler()
            print("ℹ️ Using DummyScaler (no scaling)")
        
        sys.stdout.flush()
        print("="*50 + "\n")
        sys.stdout.flush()
        
        return model, scaler
    
    except Exception as e:
        print(f"\n❌ ERROR loading model: {str(e)}")
        import traceback
        traceback.print_exc(file=sys.stdout)
        sys.stdout.flush()
        raise

class DummyScaler:
    """A dummy scaler that returns the input unchanged"""
    def __init__(self):
        self.mean_ = None
        self.scale_ = None
    
    def transform(self, X):
        return X
    
    def fit_transform(self, X):
        return X
    
    def fit(self, X):
        return self
    
    def inverse_transform(self, X):
        return X

def get_model_info():
    """Get information about the loaded model"""
    try:
        model, scaler = load_model_and_scaler()
        
        info = {
            'model_type': type(model).__name__,
            'scaler_type': type(scaler).__name__,
        }
        
        if hasattr(model, 'get_params'):
            info['model_params'] = str(model.get_params())
        
        if hasattr(model, 'n_features_in_'):
            info['n_features_in'] = model.n_features_in_
        elif hasattr(model, 'n_features_'):
            info['n_features_in'] = model.n_features_
        
        if hasattr(model, 'classes_'):
            info['classes'] = str(model.classes_)
        
        return info
    except Exception as e:
        return {'error': str(e)}
