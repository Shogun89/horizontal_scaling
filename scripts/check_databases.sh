#!/bin/bash
echo "Checking databases..."

check_databases() {
    host=$1
    result=$(mysql -h "$host" -uroot -prootpassword -e "SELECT COUNT(*) FROM users;" --skip-column-names)
    echo "$result"
}

master_a=$(check_databases "mysql-master-a")
replica_a=$(check_databases "mysql-replica-a")
master_b=$(check_databases "mysql-master-b")
replica_b=$(check_databases "mysql-replica-b")

if [ "$master_a" != "$replica_a" ]; then
    echo "WARNING: Master A ($master_a) and Replica A ($replica_a) are out of sync!"
    exit 1
fi

if [ "$master_b" != "$replica_b" ]; then
    echo "WARNING: Master B ($master_b) and Replica B ($replica_b) are out of sync!"
    exit 1
fi

echo "All databases are in sync"