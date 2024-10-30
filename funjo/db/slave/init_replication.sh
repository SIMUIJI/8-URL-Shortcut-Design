#!/bin/bash
set -e

# 슬레이브가 시작될 때 마스터에 연결하여 복제 슬롯 생성
until psql -h db-master -U user -d url_db -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

psql -h db-master -U user -d url_db -c "CREATE PUBLICATION mypub FOR ALL TABLES;"

# 복제 슬롯 생성
psql -h db-master -U user -d url_db -c "SELECT pg_create_physical_replication_slot('replication_slot');"


# 슬레이브 서버의 데이터 디렉토리
DATA_DIR="/var/lib/postgresql/data"

# standby.signal 파일 생성
touch "${DATA_DIR}/standby.signal"