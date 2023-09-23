#!/bin/bash

# Wait for the MySQL database to be available
./scripts/wait-for-it.sh db:3306 -t 60

# Start the web service
exec "$@"
