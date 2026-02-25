#!/usr/bin/env bash
set -e

source .venv/Scripts/activate

export FLASK_APP=app.py
export FLASK_DEBUG=1
echo "Starting Flask at http://localhost:5000"
flask run
