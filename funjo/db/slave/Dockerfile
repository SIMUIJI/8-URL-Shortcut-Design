# PostgreSQL 슬레이브 DB 설정
FROM postgres:latest

ENV POSTGRES_DB=url_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD='url1234'

# 슬레이브 DB 설정 관련 스크립트
COPY init_slave.sql /docker-entrypoint-initdb.d/
