# Face Recognition System (FRS) project

## Requirements

[docker](https://www.docker.com/)
[docker-compose](https://docs.docker.com/compose/)

## Further Ideas/Improvements

- Use a better way of scaling horizontally, like using Kubernetes.
- The calculated values could be distributed among a sharded database.
- The usage of a CDN and some cache in the load balancer could help accelerating some GET requests.
- Proper retry policy for semaphore handling (when Redis is down).
- Use async tasks in background for average calculation.
- Use a better way of aggregating data, instead of relying on summing on top of each value every time.

## Usage

Ensure the app is not running:

```sh
make stop
```

Start the application:

```sh
make build
make start
```
## Run tests

Unit tests:

```sh
make tests
```

## Manual testing

Note: Run the server as in the "Usage" section first.

Get face encoding for one image (replace /path/to/frs with the path of this repository in your system):

```sh
curl -w "%{http_code}" -X POST -F "upload_file=@/path/to/frs/frs/face_encodings/tests/samples/Michael_Schumacher_0003.jpg" http://localhost:8000/generate_face_encoding
```

Get face encoding for an already processed image:

```sh
curl -w "%{http_code}" http://localhost:8000/face_encoding/9300d3c14e83f9dca75e135363b4a29297a4654f521b321240b0466780c27bed
```

Check number of processed images:

```sh
curl -w "%{http_code}" http://localhost:8000/stats/
```
