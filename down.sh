set -e

if [ "$1" = "testing" ]; then
    echo Stopping testing environment...
    sudo docker compose --profile testing down -v
    sudo rm -rf ./test_node_1/test_data/
    sudo rm -rf ./test_node_2/test_data/
elif [ "$1" = "-v" ]; then
    echo Stopping deployment environment and deleting persistent data...
    sudo docker compose down -v
elif [ -z "$1" ]; then
    echo Stopping deployment environment...
    sudo docker compose down
else
    echo Unrecognized option \'$1\', please run \'$0\' without any
    echo arguments or with the argument \'testing\'.
fi
