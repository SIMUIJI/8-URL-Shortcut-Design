#!/bin/bash
set -e

cp /mnt/pg_hba.conf /var/lib/postgresql/data/pgdata/pg_hba.conf
cp /mnt/postgresql.conf /var/lib/postgresql/data/pgdata/postgresql.conf

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE url (
  short_url varchar NOT NULL,
  long_url varchar NOT NULL,
  is_enable int4 NOT NULL,
  reg_date timestamp NOT NULL,
  url_id serial4 NOT NULL,
  CONSTRAINT url_pkey PRIMARY KEY (url_id)
  );
  CREATE INDEX idx_url_long_url ON url USING btree (long_url);
  CREATE INDEX idx_url_short_url ON url USING btree (short_url);
  CREATE USER replication WITH REPLICATION LOGIN PASSWORD 'replica' CONNECTION LIMIT -1;
EOSQL