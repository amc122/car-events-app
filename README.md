# car-events-app
Simple application for data inspection, data augmentation and machine learning applied to car events audio.

## Linux

### Option 1:

Use a virtual environment to install the python dependencies in the ```requirements.txt``` file:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

then run the app using gunicorn:
```
source gunicorn_run.sh
```

### Option 2:

Build and run the Docker image using the ```Dockerfile```.

## Windows 10

The web application will only work properly in a Docker container with Linux (Ubuntu). In order to achieve this in Windows 10 you need to follow these steps:

### Step 1

Install the Windows Subsystem for Linux (WSL). Simply open PowerShell and type:
```
wsl.exe --install
``` 

Docker Desktop will require WSL 2, in order to check the WSL version type:
```
wsl -l -v
```

Example output:
```
>   NAME            STATE           VERSION
> * Ubuntu-20.04    Running         2
```

**NOTE**: If the installed Linux distribution is not version 2, it can be updated with ```wsl --set-version <NAME> 2```, e.g. ```wsl --set-version Ubuntu-20.04 2```.

### Step 2

Install Docker Desktop: 

https://docs.docker.com/desktop/windows/install/

### Step 3

Once Docker Desktop is installed, enable WSL integration with your WSL Ubuntu distro:

https://docs.docker.com/desktop/windows/wsl/

### Step 4

Finally, verify you can use docker in the WSL distro using the following command:
```
docker --version
```


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