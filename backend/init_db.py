import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import time
from models import Base
from database import get_db_url

def wait_for_db(engine, max_retries=30, retry_interval=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                print(f"Successfully connected to {engine.url}")
                return
        except OperationalError as e:
            if attempt + 1 == max_retries:
                raise
            print(f"Database connection attempt {attempt + 1} failed, retrying...")
            time.sleep(retry_interval)

def main():
    # Get shard from environment
    shard = os.getenv('SHARD')
    if not shard:
        raise ValueError("SHARD environment variable not set")

    print(f"Initializing master for shard {shard}...")
    
    # Initialize only master
    engine = create_engine(get_db_url(replica=False))
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)
    print(f"Shard {shard} master initialized")

if __name__ == "__main__":
    main()
