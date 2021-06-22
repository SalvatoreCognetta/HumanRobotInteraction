# HRI-Pepper Movies
Project for HRI course.

# How to run the application
## Run the docker image
Open a terminal
```bash
# Make sure ctc-linux-...zip, etc are in ./hri_software/docker/downloads
cd ./hri_software/docker
./build.bash # build the latest version
./run.bash
docker exec -it pepperhri tmux

```

## Run NAOqi - inside docker image
Inside the docker terminal
```bash
cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64
./naoqi
```

## Run simulator
Open Android Studio with pepper sdk installed  
- Tools > Pepper SDK > Emulator > OK

## Run scripts in the naoqi simulator
Inside the docker terminal press Ctrl+b, c (this creates a new terminal inside docker via tmux)

```bash
export PEPPER_IP=127.0.0.1 #simulation mode
cd ~/playground
python file.py
```

# Install modim

## Install tornado dependency
```bash
wget  https://bootstrap.pypa.io/pip/2.7/get-pip.py
sudo python2 get-pip.py
pip2 install tornado
```

Follow the doc in [README](./modim/README.md)