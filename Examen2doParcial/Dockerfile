#importar base de python
FROM python:3.10-slim

#Crear en el contenedor - Carpeta de trabajo
WORKDIR /code

#Copiar los requerimientos al contenedor
COPY requirements.txt /code/requirements.txt

#Instalar las dependencias de FASTAPI
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Copiar el codigo del servidor
COPY  . /code/

#Comando a ejecutar para levantar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]