FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik z zależnościami
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu aplikacji
COPY . .

# Uruchom aplikację za pomocą Gunicorn z Uvicorn workers
# Będzie nasłuchiwać na porcie podanym przez Railway w zmiennej $PORT
CMD gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:${PORT}