import os

class Config:
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    # Caching configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'RedisCache')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'redis')
    CACHE_REDIS_PORT = int(os.environ.get('CACHE_REDIS_PORT', '6379'))
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD', '')
    CACHE_REDIS_DB = int(os.environ.get('CACHE_REDIS_DB', '0'))
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_KEY_PREFIX = 'dns_by_eye_'
    CACHE_THRESHOLD = 1000  # Maximum number of items in cache
    ENABLE_CACHING = os.environ.get('ENABLE_CACHING', 'true').lower() == 'true'

    # DNS resolver timeouts
    DNS_TIMEOUT = float(os.environ.get('DNS_TIMEOUT', '2'))
    DNS_LIFETIME = float(os.environ.get('DNS_LIFETIME', '4'))

    # Enhanced rate limiting (increased for testing)
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '1000 per minute')
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'redis://redis:6379/1')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True
    
    # API specific rate limits (increased for testing)
    RATELIMIT_API_DEFAULT = '10000 per day'
    RATELIMIT_API_EXPORT = '5000 per day'
    RATELIMIT_API_DEBUG = '2000 per hour'
    
    # Request size limits
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB
    
    # Logging configuration
    LOG_FILE = 'dns_by_eye.log'
    LOG_MAX_BYTES = 10240
    LOG_BACKUP_COUNT = 10
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    
    # Version info
    VERSION = '1.3.1'
