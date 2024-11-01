# Web Server Using FastAPI

## File Structure

<pre>
├── main.py
├── domain
│   └── url
│        ├── url_crud.py
│        ├── url_router.py
│        └── url_schema.py
├── config.py
├── database.py
├── models.py
├── migrations
│   ├── versions
│   │    └── 8eea506189a2_.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── alembic.ini
├── test
│   └── test_redis.py
├── .env
├── requirements.txt
├── docker.env
├── docker-compose.yaml
└── dockerfile
</pre>

## Web Server Files

- <code>main.py</code>
  - FastAPI starting file.
- <code>domain</code>, <code>config.py</code>, <code>database.py</code>, <code>models.py</code>
  - FastAPI app directory and files.
- <code>migrations</code>, <code>alembic.ini</code>
  - This directory was created by Alembic.
  - PostgreSQL migrations.
- <code>test</code>
  - Unit test files.
- <code>.env</code>
  - Environment configuration file for web server.
  - Not used in docker container.

```.env
POSTGRES_SERVER=127.0.0.1
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
POSTGRES_PORT=5432
```

- <code>requirements.txt</code>
  - Python modules to download for starting FastAPI.

## <code>docker.env</code>

- Docker environment configuration file.

```docker.env
# Docker setting
COMPOSE_PROJECT_NAME=web-test

# Docker volume setting
WEB_WORKDIR=.

# etc setting
WEB_BINDING_PORT_1=3001
WEB_BINDING_PORT_2=3002
WEB_BINDING_PORT_3=3003
WEB_PORT=3000
```

## <code>docker-compose.yml</code>

```docker-compose.yml
version: "3.8"

services:
  web_server_1:
    container_name: web1
    build:
      context: ${WEB_WORKDIR}
      dockerfile: dockerfile
    ports:
      - ${WEB_BINDING_PORT_1}:${WEB_PORT}
    volumes:
      - ${WEB_WORKDIR}:/app
    networks:
      - web_bridge
    restart: always
  web_server_2:
    container_name: web2
    build:
      context: ${WEB_WORKDIR}
      dockerfile: dockerfile
    ports:
      - ${WEB_BINDING_PORT_2}:${WEB_PORT}
    volumes:
      - ${WEB_WORKDIR}:/app
    networks:
      - web_bridge
    restart: always
  web_server_3:
    container_name: web3
    build:
      context: ${WEB_WORKDIR}
      dockerfile: dockerfile
    ports:
      - ${WEB_BINDING_PORT_3}:${WEB_PORT}
    volumes:
      - ${WEB_WORKDIR}:/app
    networks:
      - web_bridge
    restart: always

networks:
  web_bridge:
    external: true
```

## <code>dockerfile</code>

```dockerfile
FROM python:3.12.7-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```

## Run

```bash
docker network create web_bridge
docker compose config
docker compose --env-file=docker.env up
```