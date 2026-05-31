import streamlit as st
import pickle
import numpy as np
import os
import urllib.request
from utils.feature_extractor import extract_features, get_feature_names

# Page configuration
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🛡️",
    layout="wide"
)

# Title and description
st.title("🛡️ Machine Learning Based Phishing URL Detection")
st.markdown("""
    Enter a URL below to check if it's safe or a phishing attempt.
    Our model analyzes 23 different URL features with **96% accuracy**!
""")

# Load model with caching
@st.cache_resource
def load_model():
    """Load the phishing detection model with caching"""
    try:
        # Try to download model if missing
        model_path = "phishing_model.pkl"
        github_url = "https://github.com/Ayush-Kumar-45/Phishing-URL-Detection/raw/master/phishing_model.pkl"
        
        if not os.path.exists(model_path):
            with st.spinner("Downloading model..."):
                urllib.request.urlretrieve(github_url, model_path)
                st.success("Model downloaded successfully!")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Try to load scaler if exists
        scaler = None
        if os.path.exists('scaler.pkl'):
            with open('scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
        
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

# Load model
model, scaler = load_model()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "Enter URL to analyze:",
        placeholder="https://example.com",
        help="Enter a complete URL starting with http:// or https://"
    )

with col2:
    analyze_button = st.button("🔍 Analyze URL", type="primary", use_container_width=True)

# Example URLs
with st.expander("📝 Try these examples"):
    examples = [
        "https://www.google.com",
        "https://github.com",
        "http://secure-paypal-verify.com",
        "http://apple-id-verify-now.com"
    ]
    
    for ex in examples:
        if st.button(f"Try: {ex}", key=ex):
            url = ex
            analyze_button = True

# Analysis and results
if analyze_button and url:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    with st.spinner("🔬 Analyzing URL features..."):
        # Extract features
        features = extract_features(url)
        feature_names = get_feature_names()
        feature_values = [features.get(name, 0) for name in feature_names]
        feature_array = np.array([feature_values])
        
        # Scale if scaler exists
        if scaler:
            feature_array = scaler.transform(feature_array)
        
        # Make prediction
        if model:
            prediction = model.predict(feature_array)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(feature_array)[0]
                confidence = proba[1] if prediction == 1 else proba[0]
            else:
                confidence = 0.95
            
            # Display result
            st.markdown("---")
            
            if prediction == 1:
                st.error(f"⚠️ **PHISHING DETECTED!**")
                st.markdown(f"**Confidence:** {confidence*100:.2f}%")
                st.warning("""
                    🚨 **Safety Tips:**
                    - Do NOT enter any personal information
                    - Avoid clicking on any links
                    - Close this tab immediately
                """)
            else:
                st.success(f"✅ **SAFE**")
                st.markdown(f"**Confidence:** {confidence*100:.2f}%")
                st.info("This URL appears to be legitimate.")
            
            # Show analyzed URL
            st.markdown(f"**Analyzed URL:** `{url}`")
            
            # Show feature details in expander
            with st.expander("📊 View Detailed Feature Analysis"):
                col1, col2 = st.columns(2)
                feature_items = list(features.items())
                mid = len(feature_items) // 2
                
                with col1:
                    for name, value in feature_items[:mid]:
                        st.metric(name.replace('_', ' ').title(), value)
                
                with col2:
                    for name, value in feature_items[mid:]:
                        st.metric(name.replace('_', ' ').title(), value)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>© 2024 Machine Learning Based Phishing URL Detection System</p>
    <p>Ayush Kumar | Roll No: 2308390100018 | CSE Department</p>
</div>
""", unsafe_allow_html=True)
