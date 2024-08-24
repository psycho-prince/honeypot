# Use an appropriate base image with Python installed
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
