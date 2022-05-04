# car-events-app
Simple application for data inspection and machine learning applied to car events audio.

## Build app using the Dockerfile

```
docker build -t <name>:<tag> -f Dockerfile .
```

or simply:

```
source docker_build.sh
```

## Run app using the Docker image

```
docker run -it --rm --gpus all \
    -v <absolute path to source data dir>:/data_rootdir 
    -v <absolute path to output augmented data dir>:/data_augmented
    -p 8050:8050 <name>:<tag>
```

or simply:

```
source docker_run.sh
```

## 