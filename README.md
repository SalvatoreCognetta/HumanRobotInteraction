# HRI-Pepper Movies
Project for HRI course.

# How to run the application
## Run the docker image
Open a terminal
```bash
cd ./hri_software/docker
./build.bash # build the latest version
./run.bash
docker exex -it pepperhri tmux

```

## Run NAOqi - inside docker image
In another terminal
```bash
cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64
./naoqi
```

## Run simulator
Open Android Studio with pepper sdk installed  
- Tools > Pepper SDK > Emulator > OK

## Run scripts inside naoqi simulator
Inside the docker terminal press Ctrl+b, c (this creates a new terminal inside docker via tmux)

```bash
export PEPPER_IP=127.0.0.1
cd ~/playground
python file.py
```