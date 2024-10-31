# 개발환경
- 언어 : python 3.12.7
- 프레임워크 : fastapi
- 캐시 : redis
- rdb : postgresql
----
# url 단축 기법
## 선택한 단축 기법
- base62변환 전략사용함(base62 변환은 0~9, a~z, A~Z의 62개 문자로 변환하는 것을 의미함)
## WHY?
- base62로 변환을 사용한 이유는 책에서 설명한거와 같이 충돌가능이 아예없기때문에 해당 전략 선택

## 상세설명
- 우선 base62방법은 유일한 정수ID로 base62알고리즘을 적용해야하는데 유일한 정수ID를 얻기위해 많은 방법들이있지만 캐시 저장소인 reids의 auto increment기능을 활용하여 유일한 정수ID를 얻었다.
### reids의 auto increment기능을 사용한 이유
- 이유는 각 웹서버는 하나의 캐시저장소를 본다는 가정하에 유일한 ID의 동기화는물론 빠르게 ID를 얻을수 있으므로 해당방법 선택함
### 동작방식
- url단축(post) 요청이오면 redis의 auto increment값을 1올려주고 rdb에 pk값을 해당 auto increment한 값으로 저장하고 short_url에는 base62로 변환한 값을 저장한다.
- ex : post로 url "https://www.naver.com/" 요청이오면 redis의 auto increment값은 1이되고 1을 base62로 변환하면 1이된다 그러면 short_url과 url_id에는 각각 1을넣어준다. 그리고 또다른 url post로 요청시 auto incremen값은 증가하고 증가한값에 base62를 적용한값들을 rdb에 저장한다.
----
# 실행방법
## env 설정
- src폴더에 있는 .env.example파일을 복사하여 .env파일을 만들어주고 값을넣어준다.

## 도커 네트워크
- 도커 네트워크를만들어준다 명령어 : docker network create --subnet=172.18.0.0/16 url-service-network

## 도커 컴포즈 실행
- db컴포즈를 실행후 정상적으로 동작확인후 app컴포즈를 실행합니다. db컴포즈를 먼저 실행시키는이유는 pgpool이 정상적으로 동작해야 app에서 db에 접근이가능하기때문입니다.
- db 컴포즈 실행 : docker-compose --env-file ./src/.env -f db-compose.yml up -d
- app 컴포즈 실행 : docker-compose --env-file ./src/.env -f app-compose.yml up -d
----
# 동작방식
## LoadBalancer
- Nginx에서 사용자의 요청에대해 2개의 fastapi서버로 로드밸런싱을해준다.

## fastapi
- 로드밸런서에서 넘어온 데이터를 처리해주는 서버

## redis
- 요청온 url에대해서 캐시를 해줘서 빠르게 url을 리다이렉트해준다.

## rdb
- mastre, slave로 이중화를 해서 master에는 삽입,수정,삭제 작업만하고 일기 작업은 slave에서진행
- master가 죽을시 slave가 승격하여 master역할까지함





























