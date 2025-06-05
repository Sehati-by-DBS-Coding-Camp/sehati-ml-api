# Gunakan image Python resmi
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Salin requirements jika ada, atau install Flask langsung
COPY app.py .

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port (default Flask 8080 sesuai app.py)
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "app.py"]