CONTAINER=0
INST0="cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64 && ./naoqi"
INST1="tmux new-session -d -s pepper && tmux send-keys -t pepper -l $INST0 Enter && tmux attach -t pepper"
INST2="docker exec -it pepperhri bash -c $INST1"

while [ $# -gt 0 ]; do
  case "$1" in
    --world*|-w*)
      if [[ "$1" != *=* ]]; then shift; fi # Value is next arg if no `=`
      WORLD="${1#*=}"
      ;;
    --container*|-c*)
      if [[ "$1" != *=* ]]; then shift; fi
      CONTAINER="${1#*=}"
      ;;
    --help*|-h*)
      echo "--world -w world name on which running the simulations;" # Flag argument
      echo "--container -c for running the selected container else it runs all togheter ( 1-gazebo 2-planner 3-rtabmap );"
      echo "--help -h for the help message;"
      exit 0
      ;;
    *)
      >&2 printf "Error: Invalid argument\n"
      exit 1
      ;;
  esac
  shift
done

# the $SHELL instruction permits to keep opened the bash session once the container is closed (can be useful if for instance one want to restart one container only)

case $CONTAINER in
    0 )
	sudo gnome-terminal -q --tab --title="tab 1" --command="bash -c 'cd ~/PepperProject/hri_software/docker; ./build.bash; ./run.bash; sleep(3); docker exec -it pepperhri $INST2; $SHELL; docker stop pepperhri;'" \
	--tab --title="tab 2" --command="bash -c '$SHELL'"
	;;
    1 )
	sudo gnome-terminal -q --tab --title="tab 1" --command="bash -c 'cd ~/EAI_MavSLAM/docker_app/ros_gazebo; bash ~/EAI_MavSLAM/docker_app/ros_gazebo/build.sh; sleep 1; bash ~/EAI_MavSLAM/docker_app/ros_gazebo/run.sh ${WORLD};  $SHELL'"
	;;
esac
