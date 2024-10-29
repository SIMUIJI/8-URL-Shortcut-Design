#! bin/bash

rm -rf /var/lib/postgresql/data/pgdata/*
pg_basebackup -h '172.19.0.5' -D '/var/lib/postgresql/data/pgdata' -U replication -p '5432' -v -R -P -X stream