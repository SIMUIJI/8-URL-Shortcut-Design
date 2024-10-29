# Python 3.12.7 베이스 이미지 사용
FROM python:3.12.7-bookworm

# 작업 디렉토리 설정
WORKDIR /url-shortener-secvice

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# 프로젝트 의존성 파일 복사
COPY poetry.lock pyproject.toml /url-shortener-secvice/

# Poetry를 통해 의존성 설치. 개발 의존성은 제외
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 프로젝트 파일 복사
COPY . /url-shortener-secvice

# PYTHONPATH 설정
ENV PYTHONPATH=/url-shortener-secvice/src

# 실행 권한 부여
RUN chmod +x /url-shortener-secvice/src/scripts/start.sh

# Start Gunicorn with Uvicorn
CMD ["/url-shortener-secvice/src/scripts/start.sh"]
