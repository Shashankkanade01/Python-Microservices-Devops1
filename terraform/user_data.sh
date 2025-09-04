#!/bin/bash
# Update system
yum update -y

# Install Docker
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir /app
cd /app

# Create docker-compose.yml
cat <<EOF > docker-compose.yml
version: "3.9"
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    image: shashankk01/backend:new
    environment:
      DB_HOST: postgres
      DB_NAME: mydb
      DB_USER: postgres
      DB_PASSWORD: postgres
      DB_PORT: 5432
    ports:
      - "5000:5000"
    depends_on:
      - postgres
    volumes:
      - logs:/logs

  frontend:
    image: shashankk01/frontend:new
    environment:
      BACKEND_URL: http://backend:5000/api/data
    ports:
      - "8080:8080"
    depends_on:
      - backend

  logger:
    image: shashankk01/logger:new
    depends_on:
      - backend
    volumes:
      - logs:/logs

volumes:
  pgdata:
  logs:
EOF

# Start the stack
docker-compose up -d
