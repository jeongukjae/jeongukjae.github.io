---
layout: page
title: About
permalink: /about/
---

<style>
  .page {
    overflow: hidden;
  }

  p {
    font-size: 95%;
    line-height: 1.7em;
    letter-spacing: .1px;
  }
  
  table tr {
    border-top: none;
    border-bottom: 1px solid #eee;
  }

  table tr:nth-child(2n) {
    background-color: white;
  }

  table tr td {
    border: none;
    font-size: 80%;
    padding-bottom: 20px;
    padding-top: 5px;
  }
  
  td.nowrap {
    white-space: nowrap;
  }

  small {
    font-size: 80%;
    color: #666;
  }

  blockquote {
    margin: 1em .8em;
    border-left: 2px solid #666;;
    padding: 0.1em 1em;
    color: #666;;
    font-size: 1em;
    font-style: italic;
  }

  blockquote p {
    margin: 0px;
  }

  .responsive {
    overflow-x: scroll;
  }

  table {
    width: 720px;
  }
  
  @media print {
    .wrapper-masthead, .wrapper-footer, h2#끝, h2#끝 + p {
      display: none !important;
    }
  }
</style>

<span style='display: block;text-align:right'>**정욱재**<br>
**[jeongukjae@gmail.com](mailto:jeongukjae@gmail.com)**<br>
github - **[https://github.com/JeongUkJae](https://github.com/JeongUkJae)**</span>

## 목차

1. [자기소개](#자기소개)
2. [경력](#경력)
3. [상세 경력](#상세-경력)
    1. [개인 아웃소싱](#개인-아웃소싱)
    2. [아이디얼아이디어](#아이디얼아이디어)
4. [개인 프로젝트](#개인-프로젝트)
5. [개인 활동](#개인-활동)
6. [학력](#학력)
7. [끝](#끝)

## 자기소개

주로 서버 인프라 관리(Docker, AWS) 등에 관심이 많고 서버 개발을 주로 하며, 최근에는 SPA 프레임워크/라이브러리도 관심이 많아
Vue.js를 이용한 프로젝트 또한 진행중입니다. 주로 사용하는 언어는 Python, Javascript 입니다.

오픈소스에 관심이 많습니다. [PyCon 2018](https://www.pycon.kr/2018/) 스프린트로 나온 프로젝트 중 하나인 [nirum-lang/nirum](https://github.com/nirum-lang/nirum)의 이슈들 중 문서 생성 기능 관련된 작은 이슈들을 처리하고, [CS231n_KOR_SUB](https://github.com/insurgent92/CS231N_17_KOR_SUB)라는 CS231n 강의의 한글 자막 번역 프로젝트의 자막 오타를 수정하는 등 GitHub 상의 여러가지 저장소에 기여를 하는 중입니다. 또한 Python으로 작성한 Tistory 서비스의 API 클라이언트인 [pytistory](https://github.com/JeongUkJae/pytistory)와 같은 오픈소스
프로젝트들도 작성/배포하고 있습니다.

현재 학부생 2학년입니다.

## 경력

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td>2018.01.03 - 현재</td>
      <td>아이디얼아이디어 (IdealIdea)</td>
      <td><strong>AWS 인프라 관리, 백엔드 개발</strong><br>프론트엔드 개발(Vue.js, React.js)</td>
    </tr>
  </tbody>
</table>
</div>

## 상세 경력

### 개인 아웃소싱

#### 스마트 전광판 (itstyle)

<small>2015년</small>

정부과제로 진행한 버스 전광판 컨트롤러 프로젝트입니다. 저는 안드로이드 앱 개발을 맡았으나, 지금은 PlayStore에서 찾을 수 없는 상태입니다. 아웃소싱 발주자 분이 촬영/작성하신 [Youtube 영상](https://www.youtube.com/watch?v=inFyqopE8iA), [디씨인사이드 글](http://gall.dcinside.com/board/view/?id=hit&no=13251)에 등장하는 앱을 개발하였습니다.

### 아이디얼아이디어

<small>2018.01 - 현재</small>

#### 소개

[아이디얼아이디어 웹 페이지](https://www.idealidea.co.kr/)

> 국내외 주식 투자, 금융권 출신 전문가와 함께합니다. 정확한 차트 분석과 최신 정보로 회원님들의 성공적인 투자를 도와드립니다.

> IDEAL IDEA의 개발팀은 Front/Back-end, Android, IOS 등 다양한 분야의 전문가들로 구성되어 있어 여러 분야의 개발이 가능합니다.

#### 서비스

##### LET EAT BIT

Web: [https://www.leteatbit.com/](https://www.leteatbit.com/)<br>
Android: [https://play.google.com/store/apps/details?id=kr.co.idealidea.lebit](https://play.google.com/store/apps/details?id=kr.co.idealidea.lebit)<br>
iOS: [https://itunes.apple.com/us/app/lebit/id1395991833](https://itunes.apple.com/us/app/lebit/id1395991833)

#### 프로젝트

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td class='nowrap'>2017.10 - 2018.03</td>
      <td class='nowrap'>어플리케이션 백엔드 서버 개발</td>
      <td>
        어플리케이션 서버 작성<br>
        - 기여: jwt 인증 모듈 구현 / RESTFul api / 서비스 데이터베이스 설계 / 문서화 / 단위 테스트 적용 (사내 첫 적용) / Devops (CI 서버 세팅, 자동 배포)<br>
        - stacks: python3.6 / flask / sqlalchemy / mariadb / nosetests / unittests / swagger / circleci / docker / docker-compose / Bash / AWS CodeDeploy, S3, EC2 / aws-cli
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.01 - 2018.02</td>
      <td class='nowrap'>아웃소싱</td>
      <td>
        <strong>리앤코 법무법인</strong><br>
        웹 유지보수<br>
        - 기여: UI 수정 / 일부 서버 로직 수정 (다운로드, AWS 연결) / 배포 문제 수정<br>
        - stacks: Java 1.7 / Springboot / HTML,CSS,Javascript / maven / AWS Elastic Beanstlak <br>
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.01 - 2018.03</td>
      <td class='nowrap'>아웃소싱</td>
      <td>
        <strong>주차 관리 시스템(TIS 정보통신)</strong><br>
        앱 백엔드 서버<br>
        - 기여: RESTFul api 작성 / dockerization / AWS 자동 배포 설정 <br>
        - stacks: Python 3.6 / flask / pymysql / mariadb / SQL / docker / docker-compose / AWS Codedeploy, EC2 <br><br>
        유틸 프로그램<br>
        - 기여: 이미지파일 -> 주차 위치 인식 스크립트 작성<br>
        - stacks: Python 3.6 / opencv2
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.01 - 2018.06</td>
      <td class='nowrap'>아웃소싱</td>
      <td>
        <strong>대택근무 (아뵤코리아)</strong><br>
        대시보드 작성<br>
        - 기여: UI 작성 / 서버 연결 부분 작성 / S3 배포 / CI 서버 세팅<br>
        - stacks: typescript / react / redux / material-ui / axios / tslint / babel / d3 / circleci / aws-cli / AWS S3 <br><br>
        앱 백엔드 개발<br>
        - 기여: jwt 인증 / RESTFul api / 서비스 데이터베이스 설계 / 문서화 / 단위 테스트 적용 / 웹 소켓을 이용한 실시간 API / DevOps (CI 서버 세팅, 자동 배포)<br>
        - stacks: python3.6 / flask / SocketIO / sqlalchemy / mariadb / nosetests / unittests / swagger / circleci / docker / Bash / AWS ECS, ECR, S3 / aws-cli<br>
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.7</td>
      <td class='nowrap'>웹 개발</td>
      <td>
        관리자 대시보드 작성<br>
        - 기여: UI 작성 / 인증 처리 / 단위 테스트 적용 / DevOps (CI 서버 세팅, 자동 배포) <br>
        - stacks: node.js 9.11.1 / react.js / redux / material-ui / enzyme / chai / sinon / axios / prettier / eslint / circleci / AWS S3 / aws-cli
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.6</td>
      <td class='nowrap'>유틸 프로그램 개발</td>
      <td>
        주식 관련 데이터 수집 봇<br>
        - 기여: 주식 데이터 수집 / Dockerization<br>
        - stacks: python 3.6 / requests / argparse / sqlalchemy / mariadb / docker / AWS ECS,ECR
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.06</td>
      <td class='nowrap'>유틸 프로그램 개발</td>
      <td>
        뉴스 데이터 추출<br>
        - 기여: url -> 뉴스 핵심 데이터 추출 / 서버리스 방식의 Http 서빙<br>
        - stacks: python 3.6 / zappa / flask / BeautifulSoup / OpenGraph / requests / AWS lambda, S3, apigateway
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.06 - 2018.07</td>
      <td class='nowrap'>유틸 프로그램 개발</td>
      <td>
        주식 관련 데이터 추출<br>
        - 기여: aws lambda를 이용한 스케쥴링 / 데이터베이스 상의 데이터 업데이트<br>
        - stacks: python 3.6 / serverless / BeautifulSoup / requests / AWS lambda, S3
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.10</td>
      <td class='nowrap'>웹 백엔드 서버 개발</td>
      <td>
        관리자 서버 작성<br>
        - 기여: jwt 인증 모듈 작성 / RESTFul api (결제 처리, 계정 관리, 주식 관련 CRUD, 주식 투자 정보 제공 인터페이스) / 서비스 데이터베이스 설계 / 문서화 / 단위 테스트 적용 / 커버리지 체크 / DevOps (CI 서버 세팅, 자동 배포) <br>
        - stacks: node.js 9.11.1 / koajs2 / sequelize / mariadb / jwt / prettier / eslint / jest / swagger
      </td>
    </tr>
  </tbody>
</table>
</div>

## 개인 프로젝트

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td class='nowrap'>2015.11</td>
      <td class='nowrap'>BenzeneFramework</td>
      <td>
        - <a href='https://github.com/JeongUkJae/BenzeneFramework'>GitHub Repo</a><br>
        - Java로 작성한 lightweight web framework<br>
        - 고등학생 시절 과제
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2015.12</td>
      <td class='nowrap'>Christmas-Tree-os</td>
      <td>
        - <a href='https://github.com/JeongUkJae/Christmas-Tree-os'>GitHub Repo</a><br>
        - 어셈블리로 작성한 플로피 디스크용 이미지<br>
        - just for fun
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2017.05 ~ 2018.10</td>
      <td class='nowrap'>flask jwt login</td>
      <td>
        - <a href='https://github.com/JeongUkJae/Flask-JWT-Login'>GitHub Repo</a><br>
        - 개인 프로젝트용/간단한 프로젝트용인 jwt 인증 모듈<br>
        - pip 모듈로 배포
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.06</td>
      <td class='nowrap'>서울시립대학교 학점 확인</td>
      <td>
        - <a href='https://github.com/JeongUkJae/grade-checker-uos'>GitHub Repo</a><br>
        - Typescript & React로 프론트 작성/Python & zappa로 aws lambda 이용한 serverless 서버 작성<br>
        - 학교 포털의 버그로 임시로 작성한 웹 페이지
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.02 ~ 현재</td>
      <td class='nowrap'>pytistory</td>
      <td>
        - <a href='https://github.com/JeongUkJae/pytistory'>GitHub Repo</a><br>
        - Python 3.x 버전을 지원하는 티스토리 API 클라이언트<br>
        - pip 모듈로 배포
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.08 ~ 현재</td>
      <td class='nowrap'>simple pip</td>
      <td>
        - <a href='https://github.com/JeongUkJae/simple-pip'>GitHub Repo</a><br>
        - 파이썬 패키지 관리 툴<br>
        - pip 모듈로 배포<br>
        - 개발중
      </td>
    </tr>
  </tbody>
</table>
</div>

## 개인 활동

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td class='nowrap'>2015 ~ 현재</td>
      <td class='nowrap'>설리번프로젝트</td>
      <td>
        - <a href='http://sullivanproject.in'>홈 페이지</a><br>
        - 2015.12 PHP를 이용한 웹 프로그래밍 강의 진행<br>
        - 2017.01 "취미로 하는 웹 해킹" 강의 진행<br>
        - 관련 레포지토리: <a href='https://github.com/SullivanEducation/PHP-with-Hyundai-High-School'>PHP 교육</a>
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.06 ~</td>
      <td class='nowrap'>제이펍 베타리더스 7기</td>
      <td>
        - 번역서 코드 테스트/오탈자 확인/내용 검증
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.08</td>
      <td class='nowrap'>마이크로소프트 봇 프레임워크 프로그래밍<br>베타리딩 참가</td>
      <td>
        - <a href='http://jpub.tistory.com/832?category=208491'>책 링크</a><br>
        - C#/마이크로소프트 봇 프레임워크를 이용한 챗봇 제작 튜토리얼 번역서
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.09</td>
      <td class='nowrap'>아마존 웹 서비스 부하 테스트 입문<br>베타리딩 참가</td>
      <td>
        - <a href='http://jpub.tistory.com/841?category=208491'>책 링크</a><br>
        - AWS에 배포된 웹 서버들의 부하 테스트를 설명하는 번역서
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.10</td>
      <td class='nowrap'>백설공주 거울과 인공지능 이야기<br>베타리딩 참가</td>
      <td>
        - <a href='http://jpub.tistory.com/853'>책 링크</a><br>
        - 인공지능을 쉽게 설명하는 번역서
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.09 ~ 현재</td>
      <td class='nowrap'>대학 동아리 교육 봉사</td>
      <td>
        - <a href='https://github.com/JeongUkJae/web-development-class-in-quipu'>레포지토리 링크</a>
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.11.10</td>
      <td class='nowrap'>GDG DevFest Seoul 2018 스태프</td>
      <td>
        - <a href='https://www.facebook.com/devfest.seoul.2018/'>페이스북 링크</a><br>
        - <a href='https://devfest-seoul18.gdg.kr'>홈페이지 링크</a>
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.11.15-17</td>
      <td class='nowrap'>X20 Social Hackathon 운영 스태프</td>
      <td>
        - <a href='https://www.facebook.com/X20Hackathon/'>페이스북 링크</a><br>
        - 설리번 교육 연구소에 소속되어 진행한 해커톤
      </td>
    </tr>
  </tbody>
</table>
</div>

## 학력

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td>2018.03 - 현재</td>
      <td>서울시립대학교</td>
      <td>컴퓨터과학과 학사 복수전공</td>
    </tr>
    <tr>
      <td>2018.03 - 현재</td>
      <td>서울시립대학교</td>
      <td>전자전기컴퓨터공학부 학사 재학 중</td>
    </tr>
    <tr>
      <td>2017.03 - 2018.02</td>
      <td>서울시립대학교</td>
      <td>생명과학과, 전자전기컴퓨터공학부로 전과</td>
    </tr>
    <tr>
      <td>2014.03 - 2017.02</td>
      <td>한국디지털미디어고등학교</td>
      <td>웹프로그래밍과 졸업</td>
    </tr>
  </tbody>
</table>
</div>

## 끝

제의/연락하실 일이 있으시다면, 위의 이메일로 해주시면 감사하겠습니다.
