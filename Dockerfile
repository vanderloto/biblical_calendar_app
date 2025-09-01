FROM python:3.11-slim

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Build frontend first
COPY web/frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm ci --only=production
COPY web/frontend/ ./
RUN npm run build

# Back to app directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY web/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY web/backend/ ./
COPY src/ ./src/

# Copy server file
COPY web/server.py ./

# Copy built frontend
RUN cp -r frontend/dist ./static

# Expose port
EXPOSE 10000

# Start server
CMD ["python", "server.py"]