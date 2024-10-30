# Python 기반 애플리케이션 설정
FROM python:3.9

WORKDIR /app

# 필요 라이브러리 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
