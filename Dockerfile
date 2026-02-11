FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.3

# Configure Poetry globally
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . .

# Remove poetry.toml to prevent virtualenv creation
RUN rm -f poetry.toml

# Expose port
EXPOSE 8000

# Set PYTHONPATH and run application
ENV PYTHONPATH=/app
CMD ["uvicorn", "manage:app", "--host", "0.0.0.0", "--port", "8000"]
