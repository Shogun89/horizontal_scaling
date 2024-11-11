#!/bin/bash

# Function to setup master
setup_master() {
    echo "Configuring master server..."
    host=$1
    replica_user=$2
    replica_password=$3

    # Create replication user on master
    mysql -h "$host" -uroot -prootpassword -e "CREATE USER IF NOT EXISTS '$replica_user'@'%' IDENTIFIED BY '$replica_password';"
    mysql -h "$host" -uroot -prootpassword -e "GRANT REPLICATION SLAVE ON *.* TO '$replica_user'@'%';"
    mysql -h "$host" -uroot -prootpassword -e "FLUSH PRIVILEGES;"
    
    # Get master status for replica configuration
    master_status=$(mysql -h "$host" -uroot -prootpassword -e "SHOW MASTER STATUS\G")
    echo "Master status: $master_status"
}

# Function to setup replica
setup_replica() {
    host=$1
    master_host=$2
    replica_user=$3
    replica_password=$4
    master_port=$5
    echo "Configuring replica server..."
    
    # Stop replica if running
    mysql -h "$host" -uroot -prootpassword -e "STOP SLAVE;"
    
    # Configure replica to connect to master
    mysql -h "$host" -uroot -prootpassword -e "CHANGE MASTER TO 
        MASTER_HOST='$master_host',
        MASTER_USER='$replica_user',
        MASTER_PASSWORD='$replica_password',
        MASTER_PORT=$master_port;"
    
    # Start replica
    mysql -h "$host" -uroot -prootpassword -e "START SLAVE;"
    
    # Check replica status
    replica_status=$(mysql -h "$host" -uroot -prootpassword -e "SHOW SLAVE STATUS\G")
    echo "Replica status: $replica_status"
}

# Check if SHARD environment variable is set
if [ -z "$SHARD" ]; then
    echo "Error: SHARD environment variable not set"
    exit 1
fi

echo "Setting up replication for shard $SHARD..."

if [ "$SHARD" = "a" ]; then
    setup_master "mysql-master-a" "replica_user" "replica_password"
    setup_replica "mysql-replica-a" "mysql-master-a" "replica_user" "replica_password" "3306"
elif [ "$SHARD" = "b" ]; then
    setup_master "mysql-master-b" "replica_user" "replica_password"
    setup_replica "mysql-replica-b" "mysql-master-b" "replica_user" "replica_password" "3306"
else
    echo "Error: Invalid shard '$SHARD'. Must be 'a' or 'b'"
    exit 1
fi

echo "Replication setup completed for shard $SHARD."