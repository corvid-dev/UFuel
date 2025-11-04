# Use Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy everything from the project into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Flask environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1

# Expose Flask's port
EXPOSE 5000

# Command to start Flask
CMD ["flask", "run"]
