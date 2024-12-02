set -e
xhost +local:docker
sudo docker compose up -d --build --renew-anon-volumes
