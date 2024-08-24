# Flask Honeypot System

## Overview

A Flask-based honeypot system to simulate PHP login pages and capture attack attempts.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/flask_honeypot.git
    cd flask_honeypot
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Access the application at `http://localhost` and the admin interface at `http://localhost:5000/admin`.

## Configuration

Edit `config.py` to adjust settings such as host and port.

## License

This project is licensed under the MIT License.
