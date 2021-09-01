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

# Run nginx web server
Inside a new terminal run the docker image for nginx:

```bash
export MODIM_HOME=/path/to/modim # local path to modim

# Run the web server
cd $MODIM_HOME/docker
./run_nginx.bash
```
sometimes the build fails due to other processes listening on localhost port 80, then to stop them execute:
```
sudo lsof -t -i tcp:80 -s tcp:listen | sudo xargs kill
```

To check if the web server is running open a browser at URL http://<IP_address>/<demo_folder> (IP_address can be localhost or 127.0.0.1 for the robot)

# Run MODIM web server
Copy the modim folder inside the playground (/home/playground) folder.

Inside the docker terminal press Ctrl+b, c (this creates a new terminal inside docker via tmux):

```bash
export MODIM_HOME=/home/robot/playground/modim # docker path to modim
cd $MODIM_HOME/src/GUI
python ws_server.py -robot pepper
```

# Run script for modim
Inside the docker terminal press Ctrl+b, c (this creates a new terminal inside docker via tmux):

```bash
export MODIM_HOME=/home/robot/playground/modim
cd /home/robot/playground/html/sample/scripts
python demo1.py
```

