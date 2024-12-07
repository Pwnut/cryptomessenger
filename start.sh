set -e
xhost +local:docker
sudo docker compose --profile testing up -d --build --renew-anon-volumes
#sudo docker compose up -d --build --renew-anon-volumes
