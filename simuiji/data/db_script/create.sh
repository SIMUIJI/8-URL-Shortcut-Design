#!/bin/bash
set -e

PGPASSWORD=$POSTGRESQL_PASSWORD psql -v ON_ERROR_STOP=1 --username "$POSTGRESQL_USERNAME" --dbname "$POSTGRESQL_DATABASE" <<-EOSQL
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
EOSQL