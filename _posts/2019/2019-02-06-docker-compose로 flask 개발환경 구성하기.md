---
layout: post
title: "docker-compose로 flask 개발환경 구성하기"
---

가끔 개발환경을 구성하다보면, 생각 외로 복잡해지는 경우가 있다. 그럴 때 docker로 옮겨 개발을 하는 편인데, 주로 docker-compose를 이용해 데이터베이스 서버 등등과 백엔드 서버를 같이 띄운다. 하지만 매번 할 때마다 구성이 헷갈려 한번 정리할 필요성을 느껴 정리하게 되었다.

## 프로젝트 구조 설정

```bash
.
├── .env
├── server
│   ├── Dockerfile
│   ├── app
│   │   └── app.py
│   └── requirements.txt
├── db-server
│   └── init.sql
└── docker-compose.yml
```

위의 `db-server/init.sql`은 데이터베이스 초기 설정을 위해서 넣어놓은 sql 파일이다. 다른 방식으로 구성을 하여도 물론 상관없고, 그에 따라 `docker-compose.yml`파일만 잘 수정하면 문제 없다.

## `docker-compose.yml`

`docker-compose.yml`에서는 `.env`파일을 읽어서 환경변수로 사용이 가능하다. 따라서 `docker-compose.yml`을 설정하기 전에 `.env`를 먼저 작성해준다.

```bash
MYSQL_PASSWORD=some-password
MYSQL_DATABASE=database
```

그 후 아래처럼 작성해준다. `services.db-server.enviroment`를 통해 데이터베이스를 설정하는데, 자세한 설정은 dockerhub의 mariadb를 참고하도록 하자. 나는 개발할 때 테스트용 데이터베이스를 보면서 작업하므로, 데이터베이스 포트를 접근 가능하게 설정해준다.

```yaml
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
      - '3306:3306'
  server:
    build: server/
    volumes:
      - ./server/app:/app
    depends_on:
      - db-server
    environment:
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
    ports:
      - '5000:5000'
```

## `server`

`docker-compose.yml`의 `services.server`에서 이미지를 빌드해서 사용하게 되는데, 빌드할 이미지는 `server/Dockerfile`을 통해 작성해준다. 나는 flask를 사용하므로, 아래처럼 작성해준다. 마지막 라인 두줄(COPY ~ CMD)는 앱 소스코드를 추가하고 실행하는 부분이므로, 자신의 패키지를 추가해서 실행하거나, `manage.py` 등을 이용해서 실행하자.

```dockerfile
FROM python:3.6

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/app.py /app/
CMD [ "python", "./app.py" ]
```

이렇게 하면 `server/app`이 컨테이너의 `/app`과 공유되어서 파일 변경을 감지할 수 있다.

## 실행

이렇게 파일들을 설정하고 실행하면, 다음과 같이 잘 구동이 된다.

```bash
$ docker-compose up
Creating example_db-server_1 ... done
Creating example_auth-server_1 ... done
Attaching to example_db-server_1, example_auth-server_1
db-server_1    | 2019-02-06 11:09:09 0 [Note] mysqld (mysqld 10.3.12-MariaDB-1:10.3.12+maria~bionic) starting as process 1 ...
...
정말 많은 데이터베이스 로그...
...
db-server_1    | Version: '10.3.12-MariaDB-1:10.3.12+maria~bionic'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
server_1       |  * Serving Flask app "app" (lazy loading)
server_1       |  * Environment: production
server_1       |    WARNING: Do not use the development server in a production environment.
server_1       |    Use a production WSGI server instead.
server_1       |  * Debug mode: on
server_1       |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
server_1       |  * Restarting with stat
server_1       |  * Debugger is active!
server_1       |  * Debugger PIN: 242-001-359
```

## 끝

정말 간단하게 구성한 구조이므로, 자신의 상황에 맞추어서 잘 수정해서 사용하자. 근데 이게 두가지 문제점이 있는데, 첫번째는 맨 처음 컨테이너를 띄울 때, mariadb 서버가 준비되기 전에 어플리케이션 서버가 구동이 되어서 정상적으로 연결이 안되고, 두번째는 `--force-recreate`를 사용하더라도 데이터베이스 서버는 아예 삭제되고 재생성되는 것이 아니라서 초기화 과정은 건너뛰기 때문에 정상적으로 초기회되지 않는다. 따라서 데이터베이스를 초기화하고 싶을 때는 컨테이너를 삭제하고 다시 띄우는데, 그 때마다 첫번째로 말한 문제가 계속 나타난다.

해결법은 간단한데, 개발환경임을 알리는 환경변수를 설정하고 일정한 주기마다 데이터베이스에 접속해보고 정상적으로 연결이 될 경우 서버를 키는 방법이다. ~~근데 개인 프로젝트는 귀찮아서... 그냥 쓴다..~~
