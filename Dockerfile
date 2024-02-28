FROM python:3.11.7-slim

LABEL maintainer="Bartolome Sanchez Salado"

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/app/
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/app/

WORKDIR /opt/app/frs

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
