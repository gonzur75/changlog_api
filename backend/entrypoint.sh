#!/bin/bash

python /app/app/wait_for_db.py

exec "$@"
