# Usa Python 3.10
FROM python:3.10-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone el puerto
EXPOSE 8080

# Crea el script de inicio
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
echo "Starting gunicorn..."\n\
exec gunicorn abastecedor.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info' > /start.sh

RUN chmod +x /start.sh

# Ejecuta el script de inicio
CMD ["/start.sh"]