from flask import Flask
import redis
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='honeypot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Redis
redis_client = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=os.environ.get('REDIS_PORT', 6379), db=0)

# Initialize within application context
with app.app_context():
    try:
        redis_client.ping()  # Test the Redis connection
        app.logger.info("Redis is connected!")
    except Exception as e:
        app.logger.error(f"Redis connection failed: {str(e)}")

@app.route('/')
def home():
    return "Home"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

