# car-events-app
Simple application for data inspection and machine learning applied to car events audio.

## Build instructions using the Dockerfile

```
docker build -t <name>:<tag> -f Dockerfile .
```

## Run instructions using the Docker image

```
docker run -it --rm --gpus all \
    -v <absolute path to source data dir>:/data_rootdir 
    -v <absolute path to output augmented data dir> 
    -p 8050:8050 <name>:<tag>
```