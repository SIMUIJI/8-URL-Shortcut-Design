# Cache Server Using Redis

## File Structure

<pre>
├── .env
├── docker-compose.yml
└── redis.conf
</pre>

## <code>.env</code>

- Environment configuration file.

```.env
# Docker setting
COMPOSE_PROJECT_NAME=redis-test

# Docker volume setting
REDIS_DATA_PATH=./data
REDIS_DEFAULT_CONFIG_FILE=redis.conf

# etc setting
REDIS_BINDING_PORT=6379
REDIS_PORT=6379
```

## <code>docker-compose.yml</code>

```docker-compose.yml
version: "3.8"

services:
  cache:
    container_name: redis
    image: redis:latest
    env_file: .env
    ports:
      - ${REDIS_BINDING_PORT}:${REDIS_PORT}
    command: redis-server /usr/local/etc/redis/redis.conf
    volumes:
      - ${REDIS_DATA_PATH}:/data
      - ${REDIS_DEFAULT_CONFIG_FILE}:/usr/local/etc/redis/redis.conf
    networks:
      - redis_bridge
    restart: always

networks:
  redis_bridge:
    external: true
```

## <code>redis.conf</code>

- Redis configuration file.
- <code>bind</code> option allow remote access.
  - <code>bind 127.0.0.1</code>: Only local IP
  - <code>bind 0.0.0.0</code>: All IP
- <code>requirepass</code> option set password.
- <code>protected-mode</code> option executed without any password required to access it.

## Run 

```bash
docker network create redis_bridge
docker compose config
docker compose up
```