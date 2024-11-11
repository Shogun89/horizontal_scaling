#!/bin/bash
cd /app/backend

echo "Starting database initialization..."

# Run init_db for this shard
python -m init_db

# Setup replication for this shard
source /app/scripts/enable_mysql_replication.sh

echo "Starting FastAPI application..."

uvicorn main:app --host 0.0.0.0 --port 8000 --reload 


