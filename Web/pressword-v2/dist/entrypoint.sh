#!/bin/bash

apache2-foreground &

# Function to check if the host is up
is_host_up() {
    local url="http://localhost:80"
    local response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$response" != "000" ]; then
        echo "Host is up"
        return 0
    else
        echo "Host is down. Restarting in 1 seconds..."
        return 1
    fi
}


# Check if the host is up
while ! is_host_up; do
    sleep 1
done

WP_ADMIN_USER=`cat /proc/sys/kernel/random/uuid`
WP_ADMIN_PASSWORD=`cat /proc/sys/kernel/random/uuid`

echo "Username: $WP_ADMIN_USER"
echo "Password: $WP_ADMIN_PASSWORD"

while ! wp core install --url="$WP_HOST" --title="$WP_TITLE" --admin_user="$WP_ADMIN_USER" --admin_password="$WP_ADMIN_PASSWORD" --admin_email="$WP_ADMIN_EMAIL"; do
    echo "Trying to install wordpress..."
    sleep 1
done

# wp plugin install <plugin zip to install>
wp plugin activate gadget login notes-manager

sleep infinity
