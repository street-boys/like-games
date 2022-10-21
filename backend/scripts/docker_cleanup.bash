echo "Stopping docker-compose"
docker-compose down

echo "Removing exited containers"
docker rm -v $(docker ps --filter status=dead --filter status=exited -aq)

echo "Removing dangling images"
docker rmi $(docker images -f "dangling=true" -q)

echo "Removing dangling volumes"
docker volume rm $(docker volume ls -qf dangling=true)

echo "'requires at least 1 argument(s)' just means there was nothing to clean"
echo "All Done."
