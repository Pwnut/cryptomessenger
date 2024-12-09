set -e
xhost +local:docker

if [ "$1" = "testing" ]; then
    echo Setting up testing environment...
    sudo docker compose --profile testing up -d --build --renew-anon-volumes
elif [ -z "$1" ]; then
    echo Setting up deployment environment...
    sudo docker compose up -d --build --renew-anon-volumes
else
    echo Unrecognized option \'$1\', please run \'$0\' without any
    echo arguments or with the argument \'testing\'.
fi
