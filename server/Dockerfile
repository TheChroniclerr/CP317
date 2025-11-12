# Full Python for numpy/pandas
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies (this layer is cached if requirements.txt unchanged)
RUN pip install --cache-dir=/root/.cache/pip -r requirements.txt

# Copy the rest of your source code
COPY . .

# Environment and port
ENV PORT=8080
EXPOSE 8080

# Run the app
CMD ["python", "src/main.py"]
