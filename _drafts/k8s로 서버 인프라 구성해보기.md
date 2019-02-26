---
layout: post
title: "Kubernetes로 서버 인프라 구성해보기"
tags:
---

Qwiklab과 Google Developers의 스터디잼을 통해 Kubernetes를 공부하면서, 스터디가 끝나고 각자 무언가 하나를 k8s로 구성해보기로 하였는데, 나는 직접 하나를 짜서 만들어보기로 했다. 내가 구성해볼 것으로 아래의 요구조건으로 생각을 먼저 해보았다.

1. 4개 이상의 서비스가 들어가게 만들어보자 (프론트엔드, 백엔드, 데이터베이스, 큐서버, ....)
2. 실제 어플리케이션 서버/프론트엔드 코드는 간단한 수준으로 만들어보자. **(제일 중요)**
   - 어플리케이션 코드 짜느라고 k8s에 집중 못하는 일은 없도록 하자!

이 때, redis나, 데이터베이스를 활용하게 하면서, 큐서버도 쓰게하면 좋겠다는 생각이 들어, 큐서버를 활용하면서도 간단한 앱을 생각해보니, 이미지 변환툴 하나를 만들어보자는 생각을 했다. 그래서 이미지 크기를 줄여주는 웹을 하나 만들어보기로 했다. 그리고 나중에 AWS EKS에 올려서 ELB도 달아보기로.

즉, 간단한 수준의 인증 서버를 만들고, redis를 구성하고, 이미지를 업로드하면 큐서버에 넘긴다음, 워커 컨테이너를 몇개 구성해서 워커에서 이미지 리사이징을 한 다음 이메일을 전송해주도록 해보자. ~~(어차피 개강 전의 대학생이라 시간이 많아!)~~

## 구성

- mariadb
- redis
- 인증 서버
- 이미지 변환용 서버
- 큐서버
- 이미지 변환하는 워커

위처럼 6개의 서버/워커를 구성한다.

## 준비

어차피 한번 작성하고 버릴 코드이기 때문에, python 3.x으로 짜고, 서버는 flask로 구성하자. 어차피 k8s에 올리면서 docker를 이용할 것이기 때문에 개발환경도 docker-compose로 설정해서 개발하자.

먼저 `docker-compose.yml` 부터 작성하자.

### redis & maraidb

```bash
MYSQL_PASSWORD=some-password
MYSQL_DATABASE=k8stutorial
```

```yml
version: "3.2"

services:
  db-server:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
    volumes:
      - ./db-server/init.sql:/docker-entrypoint-initdb.d/custom-init.sql
    ports:
      - "3306:3306"
  redis-server:
    image: redis:latest
```

첫번째 파일은 `.env`파일이고, 두번째 파일이 `docker-compose.yml`이다. 이렇게 작성을 하면 `./db-server/init.sql`과 `.env`의 변수들로 `db-server`의 설정이 가능해진다. 또한 지금은 개발을 하기 위한 것이니까 mariadb서버의 port를 publish 시키자.

### auth server

기본적인 인증을 담당할 `auth-server`이다. 아래처럼 생성해보자.

```bash
mkdir auth-server && cd auth-server && touch Dockerfile && mkdir app && touch app/app.py
```

`Dockerfile`에서 사용하기 위해 `requirements.txt`를 아래처럼 작성하고,

```text
Flask==1.0.2
Flask-SQLAlchemy==2.3.2
redis==3.1.0
pymysql==0.9.3
```

`Dockerfile`을 아래처럼 작성한다.

```dockerfile
FROM python:3.6

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/app.py /app/
CMD [ "python", "./app.py" ]
```

그리고 코드는 너무 길어서... [jeongukjae/k8s-tutorial](https://github.com/JeongUkJae/k8s-tutorial)의 [auth-server/app/app.py](https://github.com/JeongUkJae/k8s-tutorial/blob/master/auth-server/app/app.py)를 확인하자.

그리고 `docker-compose.yml`를 아래처럼 수정하고 확인해보자.

```yml
version: "3.2"

services:
  db-server:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
    volumes:
        - ./db-server/init.sql:/docker-entrypoint-initdb.d/custom-init.sql
  redis-server:
    image: redis:latest
  auth-server:
    build: auth-server/
    depends_on:
      - db-server
      - redis-server
    environment:
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
    ports:
      - '5000:5000'
```

그렇게 하면 5000번 포트로 정상적으로 동작하는 것을 확인할 수 있다.

### 프론트엔드 구성

그럼 이제 프론트엔드를 구성해보자. 물론 아래처럼 백엔드 컨테이너를 publish 했던 것은 모두 막고, 프론트엔드 서비스를 추가해준다.

```yml
version: "3.2"

services:
  db-server:
    image: mariadb:latest
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
    volumes:
        - ./db-server/init.sql:/docker-entrypoint-initdb.d/custom-init.sql
  redis-server:
    image: redis:latest
  auth-server:
    build: auth-server/
    depends_on:
      - db-server
      - redis-server
    environment:
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
  frontend-server:
    build: frontend-server/
    depends_on:
      - auth-server
    volumes:
      - ./frontend-server/source:/var/www
    ports:
      - '80:80'
```

nginx를 사용할 것이고, `auth-server`를 리버스 프록시 형태로 연결할 것이다. 아래처럼 nginx용 `Dockerfile`을 작성한다.

```dockerfile
FROM nginx:stable

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./source/ /var/www

CMD ["nginx", "-g", "daemon off;"]
```

그리고 `nginx.conf`를 작성한다. 루트 폴더를 위에서 사용했던 `/var/www`로 잡고, `index.html`을 메인으로 잡아준다. 그리고 `/api/auth` 경로를 `auth-server`로 리버스 프록시 형태로 연결해준다.

```conf
server {
    listen 80;
    server_name _;
    root /var/www/;
    index index.html;

    location /api/auth/ {
        proxy_pass http://auth-server:5000/;
    }
}
```

위의 설정한 파일들을 보면 알 수 있듯이 `frontend-server/source`가 프론트엔드 정적 파일들이 저장되는 경로인데, 이 부분도 너무 길어서 [frontend-server/source/index.html](https://github.com/JeongUkJae/k8s-tutorial/blob/master/frontend-server/source/index.html)로 들어가서 보자... 귀찮아서 부트스트랩을 긁어서 사용하였다.

사진 업로드/뷰어는 나중에 서버를 구성하고나서 추가한다.

### 메시지 큐 서버

이제 메시지 큐 서버를 추가해보자. 간단하게 RabbitMQ를 쓰자! RabbitMQ를 간단하게 설명하자면, Message Queue서버로 간편하게 구축 가능한 솔루션 중 하나이다. Python에서는 [pika](https://pika.readthedocs.io/en/stable/)라는 라이브러리로 rabbitmq를 연동할 수 있다. 간단하게 지금은 `docker-compose.yml`에 아래처럼 추가해놓았다.

```yml
...

  rabbitmq-server:
    image: rabbitmq:latest
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS}

...
```

### 이미지 크기 변환 툴 작성

일단 워커와 서버로 분리했다. 서버에서는 요청이 들어오면 저장과, 큐서버로의 publish만 담당하고 워커에서 실제 변환을 수행했다. 자세한 코드는 [server](https://github.com/JeongUkJae/k8s-tutorial/blob/master/resize-server/app/app.py)와 [worker](https://github.com/JeongUkJae/k8s-tutorial/blob/master/resize-worker/app/app.py)를 참고하자. `docker-compose.yml`은 아래처럼 추가하였다. 저장한 디렉토리를 공유하기 위해 설정해주었다.

```yml
...

  resize-server:
    build: resize-server/
    environment:
      - UPLOADING_PATH=/images
      - RABBITMQ_CHANNEL=${RABBITMQ_CHANNEL}
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS}
    volumes:
      - ./resize-server/app:/app
      - ./images:/images
    depends_on:
      - rabbitmq-server
      - auth-server
  resize-worker:
    build: resize-worker/
    environment:
      - UPLOADING_PATH=/images
      - RABBITMQ_CHANNEL=${RABBITMQ_CHANNEL}
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_DEFAULT_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_DEFAULT_PASS}
    volumes:
      - ./images:/images
    depends_on:
      - rabbitmq-server
      - resize-server
```
