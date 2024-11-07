FROM python:3.10-slim


# Copy the requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the working directory
WORKDIR /app

# Expose Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "generate_ticket.py"]

