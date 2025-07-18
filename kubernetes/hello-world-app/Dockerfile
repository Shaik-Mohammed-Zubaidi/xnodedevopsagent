# Use official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the app files into the container
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
