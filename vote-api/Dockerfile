# vote-api/Dockerfile

# Step 1: Use an official Python base image
FROM python:3.10-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy requirements file (if you have one)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the app code
COPY . .

# Step 6: Expose port 8000
EXPOSE 8000

# Step 7: Start the backend API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
