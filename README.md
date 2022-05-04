# car-events-app
Simple application for data inspection and machine learning applied to car events audio.

## Build instructions using the Dockerfile

```
docker build -t <name>:<tag> -f Dockerfile .
```

Example:

```
docker build -t carsoundapp:v0 -f Dockerfile .
```

## Run instructions using the Docker image

```
docker run -it --rm --gpus all \
    -v <absolute path to source data dir>:/data_rootdir 
    -v <absolute path to output augmented data dir>:/data_augmented
    -p 8050:8050 <name>:<tag>
```

Example:

```
cd ..
docker run -it --rm --gpus all \
    -v ($pwd)/data_rootdir:/data_rootdir 
    -v ($pwd)/data_augmented:/data_augmented
    -p 8050:8050 carsoundapp:v0
```

## 