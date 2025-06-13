# Gunakan image Python resmi yang ringan
FROM python:3.10-slim

# Tetapkan working directory
WORKDIR /app

# Salin requirements terlebih dahulu untuk leverage caching Docker layer
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Salin seluruh file ke image setelah dependencies
COPY . .

# Tentukan port default untuk Hugging Face Spaces
ENV PORT 7860

# Jalankan aplikasi
CMD ["python", "app.py"]
