# Load Balancer Server Using Nginx

## File Structure

<pre>
├── .env
├── docker-compose.yml
└── nginx.conf
</pre>

## <code>.env</code>

- Environment configuration file.

```.env
# Docker setting
COMPOSE_PROJECT_NAME=nginx-test

# Docker volume setting
NGINX_DEFAULT_CONFIG_FILE=.\nginx.conf
```

## <code>docker-compose.yml</code>

```docker-compose.yml
version: "3.8"

services:
  nginx:
    container_name: nginx
    image: nginx:latest
    env_file: .env
    ports:
      - 80:80
      - 443:443
    volumes:
      - ${NGINX_DEFAULT_CONFIG_FILE}:/etc/nginx/nginx.conf
    networks:
      - nginx_bridge
    restart: always

networks:
  nginx_bridge:
    external: true
```

## <code>nginx.conf</code>

- Nginx configuration file.

```nginx.conf
worker_processes 3;

events { worker_connections 1024; }

http {
  upstream node-app {
    least_conn;
    server 127.0.0.1:3001 weight=10 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3002 weight=10 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3003 weight=10 max_fails=3 fail_timeout=30s;
  }

  server {
    listen 80;

    location / {
      proxy_pass http://node-app;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      proxy_set_header Host $host;
      proxy_cache_bypass $http_upgrade;
    }
  }
}
```

## Run

```bash
docker network create nginx_bridge
docker compose config
docker compose up
```