FROM python:3.11.7-slim

LABEL maintainer="Bartolome Sanchez Salado"

RUN mkdir -p /opt/frs_tests/
WORKDIR /opt/frs_tests

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY integration .

CMD ["pytest"]
