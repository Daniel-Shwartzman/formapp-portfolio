FROM python:slim

# Set the working directory
WORKDIR /app

# Install system dependencies (including pkg-config)
RUN apt-get update && \
    apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Expose the port on which your Flask app runs
EXPOSE 5000

# Start your Flask app
CMD ["python", "app.py"]