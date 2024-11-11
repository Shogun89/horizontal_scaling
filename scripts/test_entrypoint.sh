#!/bin/bash

# Configure testing mode
TESTING="false"

echo "Hello from test container!"

# Check if TESTING variable is set to "true"
if [ "$TESTING" = "true" ]; then
    echo "Waiting 60 seconds for services to be ready..."
    sleep 60

    echo "Inserting test user via API..."
    curl -X POST http://localhost/users/ \
        -H "Content-Type: application/json" \
        -d '{"email": "test1@example.com", "is_active": true}'

    echo "Inserting test user via API..."
    curl -X POST http://localhost/users/ \
        -H "Content-Type: application/json" \
        -d '{"email": "test2@example.com", "is_active": true}'

    echo "Checking MySQL database..."
    source /app/scripts/check_databases.sh
fi

# Keep container running to inspect logs
tail -f /dev/null