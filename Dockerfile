# Usa l'immagine di base Python
FROM python:3.9

# Imposta la directory di lavoro nell'immagine del contenitore
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa le dipendenze del progetto
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice nella directory di lavoro
COPY . .

# Espone la porta 5000 (la stessa porta specificata nell'app Flask)
EXPOSE 5000

# Comando di avvio dell'applicazione Flask
CMD ["python", "app.py"]
