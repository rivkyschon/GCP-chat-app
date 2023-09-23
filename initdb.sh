#docker pull mysql:latest
docker run -d --name chat-db -e MYSQL_ROOT_PASSWORD=123 -e MYSQL_DATABASE=mydatabase -p 3306:3306 mysql:latest