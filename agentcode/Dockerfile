# Create a Dockerfile
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the necessary packages
RUN pip install -r requirements.txt

# Copy the entire app code
COPY . .

# Run the application
CMD ["python", "app.py"]
