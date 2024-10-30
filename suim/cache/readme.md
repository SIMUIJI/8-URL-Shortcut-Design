# Redis로 캐시 서버 만들기

## <code>.env</code>

- Docker Container 생성 시 참고되는 환경 설정 파일
- 현재 디렉토리에 파일 생성

```.env
# Docker setting
COMPOSE_PROJECT_NAME=

# Docker volume setting
REDIS_DATA_PATH=
REDIS_DEFAULT_CONFIG_FILE=

# etc setting
REDIS_BINDING_PORT=
REDIS_PORT=
```

## <code>redis.conf</code>

- Redis 설정파일
- <code>bind 0.0.0.0</code> 으로 설정하면 외부 IP로 Redis 접속 가능
- <code>requirepass foobared</code> 라인에 비밀 번호 설정 필요 

## 실행 

```bash
docker compose up -d
```