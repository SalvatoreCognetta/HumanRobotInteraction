# Docker file for Human Robot Interaction course
# ROS Kinetic, MARRtino, Pepper tools, MODIM, PNP
# Luca Iocchi, DIAG, Sapienza University of Rome, Italy
# Version 0.5

FROM ros:kinetic-ros-base-xenial

ARG DEBIAN_FRONTEND=noninteractive


###### USER root ######

# install libraries and ros packages 

RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && \
    apt-get install -y tmux less sudo eom wget libwebsockets-dev \
                       libxml2-dev libxml++2.6-dev flex nano unzip \
                       wget iputils-ping net-tools openssh-client \
                       bash-completion python-pip \
                       ros-kinetic-desktop ros-kinetic-navigation \
                       ros-kinetic-perception ros-kinetic-stage-ros \
                       ros-kinetic-gmapping && \
    rm -rf /var/lib/apt/lists/*


# User: robot (password: robot) with sudo power

RUN useradd -ms /bin/bash robot && echo "robot:robot" | chpasswd && adduser robot sudo

# Pepper

RUN mkdir -p /opt/Aldebaran

#-- NAOqi SDK

COPY downloads/empty downloads/naoqi-sdk-2.5.5.5-linux64.tar.gz* /opt/Aldebaran/
COPY downloads/empty downloads/ctc-linux64-atom-2.5.2.74.zip* /opt/Aldebaran/
COPY downloads/empty downloads/pynaoqi-python2.7-2.5.5.5-linux64.tar.gz* /opt/Aldebaran/

RUN if [ "$NAOQI" = "OK" ]; then \
      cd /opt/Aldebaran && \
      tar xzvf naoqi-sdk-2.5.5.5-linux64.tar.gz && \
      tar xzvf pynaoqi-python2.7-2.5.5.5-linux64.tar.gz && \
      unzip ctc-linux64-atom-2.5.2.74.zip && \
      rm naoqi-sdk-2.5.5.5-linux64.tar.gz && \
      rm pynaoqi-python2.7-2.5.5.5-linux64.tar.gz && \
      rm ctc-linux64-atom-2.5.2.74.zip && \
      cd /opt/Aldebaran/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7 && \
      chmod go+rx site-packages; \
    fi

#-- Python SDK

ENV PYTHONPATH /opt/Aldebaran/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages

###### USER robot ######

USER robot

RUN echo "set -g mouse on" > $HOME/.tmux.conf 

RUN mkdir -p $HOME/.config/pulse && \
    cd $HOME/.config/pulse && \
    ln -s /opt/config/pulse/cookie .

RUN pip install --user tornado==5.1.1

### Set up .bashrc ###

RUN echo "if [ -d /usr/lib/nvidia-384/ ]; then" >> $HOME/.bashrc
RUN echo "  export PATH=\"/usr/lib/nvidia-384/bin:\${PATH}\"" >> $HOME/.bashrc
RUN echo "  export LD_LIBRARY_PATH=\"/usr/lib/nvidia-384:/usr/lib32/nvidia-384:\${LD_LIBRARY_PATH}\" " >> $HOME/.bashrc
RUN echo "fi\n" >> $HOME/.bashrc


### Init ROS workspace ###

RUN mkdir -p $HOME/ros/catkin_ws/src

RUN /bin/bash -c "source /opt/ros/kinetic/setup.bash; cd $HOME/ros/catkin_ws/src; catkin_init_workspace; cd ..; catkin_make"

RUN echo "source $HOME/ros/catkin_ws/devel/setup.bash\n" >> $HOME/.bashrc

RUN rosdep update


### Additional packages ###

RUN mkdir -p $HOME/src/

# ROS NAOqi driver

RUN if [ "$NAOQI" = "OK" ]; then \
      cd $HOME/src && \
      git clone https://github.com/ros-naoqi/naoqi_driver.git && \
      cd $HOME/ros/catkin_ws/src && \
      ln -s $HOME/src/naoqi_driver .; \
    fi

USER root

RUN if [ "$NAOQI" = "OK" ]; then \
      apt-get update && \
      rosdep install -i -y --from-paths /home/robot/src/naoqi_driver && \
      rm -rf /var/lib/apt/lists/*; \
    fi

USER robot

# MARRtino ROS node

RUN mkdir -p $HOME/src/srrg && cd $HOME/src/srrg && \
    git clone https://gitlab.com/srrg-software/srrg_cmake_modules.git && \
    git clone https://gitlab.com/srrg-software/srrg2_orazio.git

RUN cd $HOME/ros/catkin_ws/src && \
    ln -s $HOME/src/srrg/srrg_cmake_modules . && \
    ln -s $HOME/src/srrg/srrg2_orazio .


# MARRtino apps and stage environments

RUN mkdir -p $HOME/src && \
    cd $HOME/src && \
    git clone https://github.com/robocupathomeedu/rc-home-edu-learn-ros.git && \
    git clone https://bitbucket.org/iocchi/marrtino_apps.git && \
    git clone https://bitbucket.org/iocchi/stage_environments.git && \
    git clone https://github.com/Imperoli/gradient_based_navigation.git 

RUN cd $HOME/ros/catkin_ws/src && \
    ln -s $HOME/src/stage_environments . && \
    ln -s $HOME/src/gradient_based_navigation .

RUN echo "export MARRTINO_APPS_HOME=$HOME/src/marrtino_apps" >> $HOME/.bashrc
RUN echo "export ROBOT_TYPE=stage\n" >> $HOME/.bashrc


# Petri Net Plans

RUN cd $HOME/src && git clone https://github.com/iocchi/PetriNetPlans

RUN cd $HOME/src/PetriNetPlans/PNP &&  mkdir -p build &&  cd build  &&  cmake ..  && make
RUN cd $HOME/src/PetriNetPlans/PNPgen &&  mkdir -p build &&  cd build  &&  cmake ..  && make

RUN echo "export PNP_HOME=$HOME/src/PetriNetPlans\n" >> $HOME/.bashrc


USER root

RUN cd /home/robot/src/PetriNetPlans/PNP/build && make install
RUN cd /home/robot/src/PetriNetPlans/PNPgen/build && make install
RUN cd /usr/local/bin && ln -sf /home/robot/src/PetriNetPlans/Jarp/scripts/jarp.sh .

USER robot

RUN cd $HOME/ros/catkin_ws/src && \
    ln -s $HOME/src/PetriNetPlans/PNPros/ROS_bridge/pnp_msgs . && \
    ln -s $HOME/src/PetriNetPlans/PNPros/ROS_bridge/pnp_ros .


# MODIM

# Mounted from local host
# RUN cd $HOME/src && git clone https://bitbucket.org/mtlazaro/modim.git

RUN echo "export MODIM_HOME=\$HOME/src/modim\n" >> $HOME/.bashrc


# Pepper tools

# Mounted from local host
# RUN cd $HOME/src && git clone https://bitbucket.org/mtlazaro/pepper_tools.git

RUN echo "export PEPPER_TOOLS_HOME=\$HOME/src/pepper_tools" >> $HOME/.bashrc

RUN echo "export PEPPER_IP=127.0.0.1\n" >> $HOME/.bashrc


# Compile ROS packages

RUN /bin/bash -c "source $HOME/ros/catkin_ws/devel/setup.bash; cd $HOME/ros/catkin_ws; catkin_make"


# Set working dir and container command

WORKDIR /home/robot

CMD /usr/bin/tmux


