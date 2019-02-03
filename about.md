---
layout: page
title: About
permalink: /about/
---

<style>
  #main .page {
    overflow: hidden;
  }

  #main p {
    font-size: 95%;
    line-height: 1.7em;
    letter-spacing: .1px;
  }
  
  #main table tr {
    border-top: none;
    border-bottom: 1px solid #eee;
  }

  #main table tr:nth-child(2n) {
    background-color: white;
  }

  #main table tr td {
    border: none;
    font-size: 80%;
    padding-bottom: 20px;
    padding-top: 5px;
  }
  
  #main td.nowrap {
    white-space: nowrap;
  }

  #main .responsive {
    overflow-x: scroll;
  }

  #main table {
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

## 자기소개

주로 서버 인프라 관리(Docker, AWS) 등에 관심이 많고 서버 개발을 주로 하며, 최근에는 SPA 프레임워크/라이브러리도 관심이 많아
Vue.js를 이용한 프로젝트 또한 진행중입니다. 주로 사용하는 언어는 Python, Javascript 입니다.

오픈소스에 관심이 많습니다. [PyCon 2018](https://www.pycon.kr/2018/) 스프린트로 나온 프로젝트 중 하나인 [nirum-lang/nirum](https://github.com/nirum-lang/nirum)의 이슈들 중 문서 생성 기능 관련된 작은 이슈들을 처리하고, [CS231n_KOR_SUB](https://github.com/insurgent92/CS231N_17_KOR_SUB)라는 CS231n 강의의 한글 자막 번역 프로젝트의 자막 오타를 수정하는 등 GitHub 상의 여러가지 저장소에 기여를 하는 중입니다. 또한 Python으로 작성한 Tistory 서비스의 API 클라이언트인 [pytistory](https://github.com/JeongUkJae/pytistory)와 같은 오픈소스
프로젝트들도 작성/배포하고 있습니다.

현재 서울시립대학교 전자전기컴퓨터공학부/컴퓨터과학부 재학중인 학부생 3학년입니다.

## 경력

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td>2018.01.03 - 현재</td>
      <td>아이디얼아이디어 (IdealIdea)</td>
      <td>AWS 인프라 관리, 백엔드 개발<br>프론트엔드 개발(Vue.js, React.js)</td>
    </tr>
  </tbody>
</table>
</div>

## 상세 경력

### 개인 아웃소싱

#### 스마트 전광판 (itstyle, 2015년)

정부과제로 진행한 버스 전광판 컨트롤러 프로젝트입니다. 저는 안드로이드 앱 개발을 맡았으나, 지금은 PlayStore에서 찾을 수 없는 상태입니다. 아웃소싱 발주자 분이 촬영/작성하신 [Youtube 영상](https://www.youtube.com/watch?v=inFyqopE8iA), [디씨인사이드 글](http://gall.dcinside.com/board/view/?id=hit&no=13251)에 등장하는 앱을 개발하였습니다.

### 아이디얼아이디어 (2018년)

[아이디얼아이디어 웹 페이지](https://www.idealidea.co.kr/)

#### 서비스

##### LET EAT BIT

[Web](https://www.leteatbit.com/), [Android](https://play.google.com/store/apps/details?id=kr.co.idealidea.lebit), [iOS](https://itunes.apple.com/us/app/lebit/id1395991833)

#### 프로젝트

<div class='responsive'>
<table>
  <tbody>
    <tr>
      <td class='nowrap'>2017.10 - 2018.03</td>
      <td class='nowrap'>어플리케이션 백엔드 서버 개발</td>
      <td>
        어플리케이션 서버 작성<br> python3.6 / flask / sqlalchemy / mariadb / nosetests / unittests / swagger / circleci / docker / Bash / AWS CodeDeploy, S3, EC2 / aws-cli
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.01 - 2018.03</td>
      <td class='nowrap'>아웃소싱</td>
      <td>
        <strong>주차 관리 시스템(TIS 정보통신)</strong><br>
        앱 백엔드 서버<br> Python 3.6 / flask / pymysql / mariadb / SQL / docker / AWS Codedeploy, EC2 / opencv2
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.01 - 2018.06</td>
      <td class='nowrap'>아웃소싱</td>
      <td>
        <strong>대택근무 (아뵤코리아)</strong><br>
        typescript / react / redux / material-ui / tslint / d3 / circleci / aws-cli / AWS S3 / python3.6 / flask / SocketIO / sqlalchemy / mariadb / swagger / circleci / docker / AWS ECS, ECR, S3 / aws-cli
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.7</td>
      <td class='nowrap'>웹 개발</td>
      <td>
        관리자 대시보드 작성<br>
        node.js 9.11 / react.js / redux / material-ui / enzyme / prettier & eslint / circleci / AWS S3 / aws-cli
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.6</td>
      <td class='nowrap'>내부 데이터 수집 봇</td>
      <td>
        python 3.6 / zappa / flask / requests / argparse / sqlalchemy / mariadb / docker / AWS ECS,ECR,lambda
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.05 - 2018.10</td>
      <td class='nowrap'>웹 백엔드 서버 개발</td>
      <td>
        node.js 9.11 / koajs2 / sequelize / mariadb / jwt / prettier / eslint / jest / swagger
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
      <td class='nowrap'>2017.05 ~ 2018.10</td>
      <td class='nowrap'>flask jwt login</td>
      <td>
        - <a href='https://github.com/JeongUkJae/Flask-JWT-Login'>GitHub Repo</a><br>
        - 개인 프로젝트용/간단한 프로젝트용인 jwt 인증 모듈<br>
        - pip 모듈로 배포
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
    <tr>
      <td class='nowrap'>2018.12</td>
      <td class='nowrap'>인스파이어드; 개정보증판<br>베타리딩 참가</td>
      <td>
        - <a href='http://jpub.tistory.com/879'>책 링크</a><br>
        - 제품 관리자들을 위한 책
      </td>
    </tr>
    <tr>
      <td class='nowrap'>2018.12</td>
      <td class='nowrap'>리액트 인 액션 베타리딩 참가</td>
      <td>
        - <a href='http://jpub.tistory.com/893'>책 링크</a><br>
        - 원서 : <a href='https://www.manning.com/books/react-in-action'>Manning - React in Action</a>
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
      <td>컴퓨터과학부 학사 복수전공</td>
    </tr>
    <tr>
      <td>2017.03 - 현재</td>
      <td>서울시립대학교</td>
      <td>전자전기컴퓨터공학부 학사 재학 중</td>
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
