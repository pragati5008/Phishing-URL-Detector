import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Model paths
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    # Logging
    LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_LEVEL = 'INFO'
    
    # Session
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    
    # API rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per day"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
    # Production settings
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Select configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}