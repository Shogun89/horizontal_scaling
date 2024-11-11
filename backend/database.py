import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_db_url(replica: bool = False) -> str:
    """
    Get database URL based on environment variable SHARD
    
    Args:
        replica (bool): If True, connect to replica instead of master
    
    Returns:
        str: Database connection URL
    """
    shard = os.getenv('SHARD', 'a')  # Default to a if not set
    replica_suffix = 'replica' if replica else 'master'
    return f"mysql://root:rootpassword@mysql-{replica_suffix}-{shard}:3306/fastapi_db"

def get_db_session(replica: bool = False):
    """Get database session for this API instance's shard"""
    engine = create_engine(get_db_url(replica))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
