# PostgreSQL 마스터 DB 설정
FROM postgres:latest

ENV POSTGRES_DB=url_db
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=url1234

# 데이터베이스 초기화 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/
