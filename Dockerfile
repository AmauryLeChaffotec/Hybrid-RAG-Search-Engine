FROM python:3.11-slim

WORKDIR /app

# Install system build dependencies required by some sentence-transformers wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer cache optimisation)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project
COPY . .

# Runtime environment variables (override at container start)
ENV MISTRAL_API_KEY=""
ENV PYTHONPATH=/app

# Default: print help. Override CMD at runtime for actual usage:
#   docker run --rm -e MISTRAL_API_KEY=xxx rag-engine index --docs docs/
#   docker run --rm -e MISTRAL_API_KEY=xxx rag-engine search -q "What are GDPR retention rules?"
EXPOSE 8000

CMD ["python", "-m", "src.main", "--help"]
