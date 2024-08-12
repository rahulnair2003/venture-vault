#!/bin/bash

print_message() {
    echo "================================================="
    echo $1
    echo "================================================="
}

check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "$1 could not be found, please install it."
        exit 1
    fi
}

print_message "Checking pre-requisites..."
check_tool python3
check_tool node
check_tool yarn
check_tool flask

print_message "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate


print_message "Installing Python dependencies..."
pip install -r requirements.txt
print_message "Installing Node dependencies..."
cd frontend && yarn && cd ..

print_message "Indexing articles from news api..."
flask create-index


run_flask_and_frontend() {
    print_message "Launching API app..."
    flask run &
    FLASK_PID=$!

    print_message "Launching frontend app..."
    cd frontend && yarn start &
    FRONTEND_PID=$!

    trap "kill $FLASK_PID $FRONTEND_PID" EXIT

    wait $FLASK_PID $FRONTEND_PID
}

run_flask_and_frontend
