import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    """基礎配置類"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # YouTube API 配置
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    YOUTUBE_API_SERVICE_NAME = os.environ.get('YOUTUBE_API_SERVICE_NAME', 'youtube')
    YOUTUBE_API_VERSION = os.environ.get('YOUTUBE_API_VERSION', 'v3')
    
    # YouTube Analytics API 配置
    YOUTUBE_ANALYTICS_API_SERVICE_NAME = os.environ.get('YOUTUBE_ANALYTICS_API_SERVICE_NAME', 'youtubeAnalytics')
    YOUTUBE_ANALYTICS_API_VERSION = os.environ.get('YOUTUBE_ANALYTICS_API_VERSION', 'v2')
    
    # Google OAuth 配置
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/callback')
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # 緩存配置
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # 速率限制配置
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False

class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

