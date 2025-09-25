FROM python:3.11-slim

# Evitar buffer en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Ejecutar gunicorn en producción, pero para pruebas usaremos runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
