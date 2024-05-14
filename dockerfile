# Usar una imagen base de Python
FROM python:3.11

# Establecer un directorio de trabajo
WORKDIR /app

# Instalar el comando ping // la imagen de debian que se usa para el docker,
# no viene con el comando 'ping' instalado
RUN apt-get update && apt-get install -y inetutils-ping

# Copiar los archivos de requisitos e instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "./main.py"]
