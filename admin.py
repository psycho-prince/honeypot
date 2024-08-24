from flask import Flask, render_template
import logging

app = Flask(__name__)

@app.route('/admin')
def admin():
    with open('honeypot.log', 'r') as file:
        logs = file.readlines()
    return render_template('admin.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
