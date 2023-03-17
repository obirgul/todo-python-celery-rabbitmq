import logging
import os
import sys
# import sqlalchemy as sql

# from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

config_class = os.environ.get("APP_CONFIG", "Config")
config = getattr(__import__("app_config", fromlist=[config_class]), config_class)

# engine = sql.create_engine(config.DATABASE_URI, pool_size=50, max_overflow=0)
# session = sessionmaker(bind=engine)
# Base.metadata.create_all(bind=analyticsdb, checkfirst=True)

# analyticsdb = sql.create_engine(config.ANALYTICS_URI, pool_size=50, max_overflow=0)
# analytics_session = sessionmaker(analyticsdb)
