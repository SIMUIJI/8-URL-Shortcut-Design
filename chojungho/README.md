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



