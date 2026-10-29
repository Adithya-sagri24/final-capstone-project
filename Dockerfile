FROM python:3.9-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY service/ ./service/

# Create a non-root user and change ownership
RUN useradd --uid 1000 theia && chown -R theia /app
USER theia

# Expose port and define entrypoint
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]

