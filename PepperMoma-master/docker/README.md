# DOCKER INSTALLATION TO REPRODUCE THE EXPERIMENTS

This instructions were made by [Prof. Iocchi](https://sites.google.com/a/dis.uniroma1.it/iocchi/) for the 2020 course in [Human-Robot Interaction](https://sites.google.com/a/dis.uniroma1.it/human-robot-interaction/) at [Sapienza University of Rome](www.uniroma1.it). 

## Install [docker](www.docker.com)

Linux version suggested. See also 
[Post-installation steps for Linux](https://docs.docker.com/install/linux/linux-postinstall/),
in particular, add your user to the `docker` group and log out and in again, before proceeding.


## Download SoftBank SDK

This is an optional step if you want to connect to SoftBank Nao or Pepper robots.

Download the following SDK from SoftBank web site and place them in `docker/downloads` folder.

    naoqi-sdk-2.5.5.5-linux64.tar.gz
    ctc-linux64-atom-2.5.2.74.zip
    pynaoqi-python2.7-2.5.5.5-linux64.tar.gz


## Configure your system (host OS)

Note: If you want to use different folders, duplicate and modify the `run.bash` script with your own folders. Do not change `run.bash` directly.


1) Download [modim](https://bitbucket.org/mtlazaro/modim) in default location `$HOME/src/modim`

    cd $HOME/src
    git clone https://bitbucket.org/mtlazaro/modim.git


2) Download [pepper_tools](https://bitbucket.org/mtlazaro/pepper_tools) in default location `$HOME/src/Pepper/pepper_tools`

Not needed if you are not planning to use Nao or Pepper robots.

    mkdir -p $HOME/src/Pepper
    cd $HOME/src/Pepper
    git clone https://bitbucket.org/mtlazaro/pepper_tools.git 


3) Create a folder `$HOME/playground` that will be shared with the docker container.

    mkdir -p $HOME/playground

This folder will contain permanent files (i.e., files that will survive docker container execution).
Any other file saved in other folders of the docker container will be lost when the container is closed.


4) Update the repositories

If needed, update the repositories from your host system

    cd $HOME/src/Pepper/pepper_tools
    git pull

    cd $HOME/src/modim
    git pull

You don't need to make any change in the image, as these folders are mounted
from your system and since they contain only Python script code, you do not need to
recompile in the container.


## Build an image

Latest version

    ./build.bash 

Specific version

    ./build.bash <version> Dockerfile_<version>

Example:

    ./build.bash 0.4.1 Dockerfile_0.4.1



To build an image ignoring cached steps, use:

    ./build.bash <version> <Dockerfile> --no-cache

Example:

    ./build.bash 0.4.1 Dockerfile_0.4.1 --no-cache


Note: `build` script will tag the last built image as `latest`


## Run an image

Latest version

    ./run.bash

Specific version (e.g. 0.4.1)

    ./run.bash <version>

Example:

    ./run.bash 0.4.1


This docker image uses [tmux](https://github.com/tmux/tmux/wiki) as  terminal multiplexer.


## Update an image

For permanent changes of your image, when the container is running, you can use

    docker commit <container_name> <image_name>

`<image_name>` can be either a new name or replace the current one


## Delete an image

Images use several GB of disk space. If you want to remove an image you are not using anymore, use the following commands:

    docker image ls
    REPOSITORY                TAG     IMAGE ID         ...
    image-you-want-to-delete  0.0     6b82ade82afd     ...
        
    docker image rm -f <IMAGE ID>


## Cleaning dangling images and containers

    docker image prune
    docker container prune

----

# Web server

A web server is used by MODIM to display HTML pages on Pepper tablet.
Install a web server on your laptop as an additional docker container.
Make sure you do not have a web server already running on your system.


## Configure your host OS

Create a folder that will contain HTML files of your project.

    mkdir -p $HOME/playground/html

Create a simple `index.html` file

    echo "<h1>Welcome</h1>" > $HOME/playground/html/index.html


## Build the nginx image

    cd docker
    ./build.bash nginx Dockerfile_nginx

## Run the nginx image

    cd docker
    ./run_nginx.bash

This is a blocking command (see how to quit the web server later)

## Test the web server

Open a browser and load the URL `http::/localhost/` (or `http://<YOUR_IP_ADDRESS>/`)

## Quit the web server

Type `CTRL-c` on the terminal running `run_nginx.bash` or use  `docker container stop <CONTAINER ID>`