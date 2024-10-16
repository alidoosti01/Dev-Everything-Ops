FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
COPY app.py .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
