FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
# ENV BOT_TOKEN='MY_BOT_TOKEN' 

# Run the bot
CMD ["python", "main.py"]
