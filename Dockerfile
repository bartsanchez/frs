FROM python:3.11.7-slim

LABEL maintainer="Bartolome Sanchez Salado"

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    git \
    build-essential \
    cmake \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


# Install DLIB
RUN cd ~ && \
    mkdir -p dlib && \
    git clone https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install

# Install lib for caching Docker layer and speed up the build
RUN pip install face-recognition==1.3.0

RUN mkdir -p /opt/app/
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/app/

WORKDIR /opt/app/frs

EXPOSE 8000

CMD ["uvicorn", "frs.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
