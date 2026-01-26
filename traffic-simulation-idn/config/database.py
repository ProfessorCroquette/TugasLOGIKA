"""
Database configuration
"""

from config.settings import DATABASE_URL

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = DATABASE_URL
SQLALCHEMY_ECHO = True  # Set to False in production
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_POOL_PRE_PING = True
SQLALCHEMY_MAX_OVERFLOW = 20

# Alembic configuration
ALEMBIC_VERSION_TABLE = "alembic_version"

# Connection options
CONNECTION_TIMEOUT = 30
AUTOCOMMIT = False
AUTOFLUSH = True
EXPIRE_ON_COMMIT = True
