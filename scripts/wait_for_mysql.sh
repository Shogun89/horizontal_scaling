#!/bin/bash
echo "Waiting for MySQL instances..."

wait_for_mysql() {
    host=$1
    counter=0
    
    while ! mysql -h "$host" -uroot -prootpassword -e "SELECT 1" >/dev/null 2>&1; do
        echo -n "."  # Print dots to show progress
        if [ $((counter % 30)) -eq 0 ]; then  # Print hostname every 30 seconds
            echo
            echo "Waiting for $host..."
        fi
        counter=$((counter + 1))
        sleep 1
    done
    
    echo
    echo "Connected to $host"
}

# Wait for each MySQL instance
wait_for_mysql "mysql-master-a"
wait_for_mysql "mysql-replica-a"
wait_for_mysql "mysql-master-b"
wait_for_mysql "mysql-replica-b"

echo "MySQL instances are ready."