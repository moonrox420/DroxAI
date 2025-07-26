# DroxAI Platform Docker Configuration
# Multi-stage build for production deployment

# Stage 1: Backend
FROM python:3.12-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# Stage 2: Frontend build
FROM node:20-alpine as frontend-build

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ .

# Build the frontend
RUN npm run build

# Stage 3: Production
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy backend from stage 1
COPY --from=backend /app/backend ./backend
COPY --from=backend /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin

# Copy built frontend from stage 2
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Create necessary directories
RUN mkdir -p /app/logs /var/log/supervisor

# Copy startup scripts
COPY run_all.sh quick_start.sh ./
RUN chmod +x *.sh

# Expose ports
EXPOSE 80 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command to run the platform
CMD ["./quick_start.sh"]