# Postgres로 DB 이중화 및 백업 기능 설정

## Network

- Set up network.

```shell
docker network create pg_bridge
```

## Primary DB

- Set up primary postgres instance and backup.

```shell
# Run primary container 
cd 8-URL-Shortcut-Design/suim/db_ha
docker run -it --rm --name pg1 \
--net pg_bridge \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=postgresdb \
-e PGDATA="/data" \
-v $PWD/postgres-primary/pgdata:/data \
-v $PWD/postgres-primary/config:/config \
-v $PWD/postgres-primary/archive:/archive \
-p 5000:5432 \
postgres:15 -c 'config_file=/config/postgresql.conf'

# Create a new user
docker exec -it pg1 bash
createuser -U postgres -P -c 5 --replication replicationUser
exit

# Run backup container 
cd 8-URL-Shortcut-Design/suim/db_ha
docker run -it --rm \
--network postgres \
-v ${PWD}/postgres-secondary/pgdata:/data \
--entrypoint /bin/bash postgres:15

# 
pg_basebackup -h pg1 -p 5432 -U replicationUser -D /data/ -Fp -Xs -R
```

## Standby DB

- Set up standby postgres instance.

```shell
# Run standby container 
cd 8-URL-Shortcut-Design/suim/db_ha
docker run -it --rm --name pg2 \
--net pg_bridge \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=postgresdb \
-e PGDATA="/data" \
-v ${PWD}/postgres-secondary/pgdata:/data \
-v ${PWD}/postgres-secondary/config:/config \
-v ${PWD}/postgres-secondary/archive:/mnt/server/archive \
-p 5001:5432 \
postgres:15 -c 'config_file=/config/postgresql.conf'
```

# 참고문헌
[High Availability in PostgreSQL: Replication with Docker](https://vuyisile.com/high-availability-in-postgresql-replication-with-docker/)
