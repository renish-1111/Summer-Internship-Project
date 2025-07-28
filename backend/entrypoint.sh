#!/bin/bash
set -e

# Initialize migrations if not exists
if [ ! -d "migrations" ]; then
  flask db init
fi

# Generate new migration (safe if no changes)
flask db migrate -m "Auto migration"

# Apply migrations
flask db upgrade

# Run the app
python run.py
