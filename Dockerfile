FROM python:3.11-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik z zależnościami
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu aplikacji
COPY . .

# Uruchom aplikację za pomocą serwera produkcyjnego Gunicorn
# Będzie nasłuchiwać na porcie podanym przez Railway w zmiennej $PORT
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]