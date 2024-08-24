from flask import Flask, render_template
import logging

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    try:
        with open('honeypot.log', 'r') as log_file:
            logs = log_file.readlines()
    except FileNotFoundError:
        logs = []

    return render_template('dashboard.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
