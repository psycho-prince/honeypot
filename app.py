from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import redis
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

# Configure logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT', 587)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Configure Redis for rate limiting
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 8080),
    db=0
)

# Configure Flask-Limiter with Redis storage
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', 8080)}"
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define User class for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.before_request
def check_redis_connection():
    try:
        redis_client.ping()  # Test the Redis connection
        app.logger.info("Redis is connected!")
    except Exception as e:
        app.logger.error(f"Redis connection failed: {str(e)}")

@app.route('/')
def home():
    return "Welcome to the Flask Honeypot!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        app.logger.info(f"Contact form submitted by {name}: {message}")
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    # Simulate SQL query (dangerous in real life, but fine here for demonstration)
    result = f"Results for '{query}'"
    return render_template('search_results.html', result=result)

@app.route('/echo', methods=['GET'])
def echo():
    user_input = request.args.get('input', '')
    return f"User input: {user_input}"

@app.route('/admin')
@login_required  # Optional: Use if you want this page restricted to logged-in users
def admin():
    return render_template('admin.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
