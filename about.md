---
layout: page
title: About
permalink: /about/
---

현재 스캐터랩의 핑퐁팀에서 머신러닝 소프트웨어 엔지니어로 재직중입니다. 주로 서버 인프라/백엔드에 관심이 많고, 취미로 프론트엔드, 머신러닝 등등을 공부합니다.

개인적으로 공부한 것을 쌓아놓는 용도로 사용하는 블로그입니다. 공부를 하시는 분들께 도움이 되었으면 좋겠습니다. 혹시나 잘못된 내용이 있다거나 말씀해주실 다른 내용이 있으시다면 블로그 하단의 이메일 아이콘을 클릭하셔서 보내주시면 감사하곘습니다.

* [링크드인](https://www.linkedin.com/in/jeongukjae/)
* [GitHub](https://www.github.com/jeongukjae/)

## 포스트 수

총 포스트 수: {{ site.posts | size }}개

{% assign number_of_posts = 0 %}
{% for post in site.posts %}{% assign currnet_year = post.date | date: "%Y" %}{% assign previous_year = post.previous.date | date: "%Y" %}{% assign number_of_posts = number_of_posts | plus: 1 %}{% if currnet_year != previous_year %}
* {{ currnet_year }}년 : {{ number_of_posts }}개의 포스트{% assign number_of_posts = 0 %}{% endif %}{% endfor %}
