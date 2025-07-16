FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE $PORT

# Run migration and start the Django server
CMD ["sh", "-c", "until pg_isready -h db -p 5432 -U sportadmin; do echo 'Waiting for PostgreSQL...'; sleep 1; done;python manage.py makemigrations && python manage.py migrate && python manage.py makemigrations installations && python manage.py migrate installations && python manage.py makemigrations authentication && python manage.py migrate authentication && python manage.py load_csv data/filtered-data-es.csv || true && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"]