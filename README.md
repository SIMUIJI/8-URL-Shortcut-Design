# 8-URL Shortcut Design

## 주요기능

1. url단축 : 주어진 긴 url을 훨씬 짧게 줄인다.
2. url 리디렉션 : 축약된 url로 http 요청이 오면 원래 url로 안내
3. 높은 가용성가 규모 학장성, 그리고 장애 감내 요구
---

## 제한사항

1. 단축 url은 숫자 0부터9까지와 영문자 a부터z, A부터Z 만 사용할수 있다.
2. 시스템을 단순화 하기 위해 삭제나 갱신은 할수없다고 가정한다

---

## API 엔드포인트

**API 통신 형식**

- RESTful API

**통신 메서드**

- GET /api/v1/shortUrl
    - 인자 : {longUrl : longURLstring}
    - 반환 : 단축 URL
- POST /api/v1/shorten
    - 반환 : HTTP 리디렉션 목저지가 될 원래 URL

**상태코드**

- 301 or 302 중에 더적합하다고 생각한걸 조사후 사용하기

---

## 스키마

**CREATE** **TABLE** url (

short_url **varchar** **NOT** **NULL**,

long_url **varchar** **NOT** **NULL**,

is_enable **int4** **NOT** **NULL**,

reg_date **timestamp** **NOT** **NULL**,

url_id serial4 **NOT** **NULL**,

**CONSTRAINT** url_pkey **PRIMARY** **KEY** (url_id)

);

**CREATE** **INDEX** idx_url_long_url **ON** url **USING** btree (long_url);

**CREATE** **INDEX** idx_url_short_url **ON** url **USING** btree (short_url);

---

## url 단축 기법

- hash value 길이는 7로
- 해시 후 충돌 해소전략 or base62변환 방법중 하나 선택하여 진행
### 해시 후 충돌 해소전략
- CRC32, MD5, SHA-1 등 해시함수적용후 앞7자리만 저장한다 만약 충돌시 사전에 입력한 문자열을 더해서 저장한다
### base62변환 전략
- url을 유일생성ID로 변환한뒤 base62를 이용하여 인코딩해준다 예를들어 https://en.wikipedia.org/wiki/Systems_design 이라고 url이 있으면 유일 ID생성기로 반환하면 2009215674938이 되겠고 base62로 변환하면 zn9edcu가 된다.

---

## 아키텍처

![image](https://github.com/user-attachments/assets/57d4da31-ced4-4044-b6ec-189df523c21d)

요청 → 로드밸런서 → 캐시 or 데이터베이스 와같은 아키텍처로 구성한다

웹서버는 2개이상, 데이터베이스는 master, slave로 구성을한다.

---

## 최종흐름

1. 사용자가 단축 url 클릭
2. 로드밸랜서가 해당 클릭으로 발생한 요청을 웹 서버에 전달
3. 단축 url이 이미 캐시에 있으면 원래 url을 꺼내서 클라이언트에 전달
4. 캐시에 해당 단축 url이 없으면 데이터베이스에서 깨낸다. 데이터베이스에 없다면 아마 사용자가 잘못된 단축 url을 입력한 경우일 것이다.
5. 데이터 베이스에서 꺼낸 url을 캐시에 넣은 후 사용자에게 반환한다.
