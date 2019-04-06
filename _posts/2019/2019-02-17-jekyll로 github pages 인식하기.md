---
layout: post
title: "Jekyll로 github pages 인식하기"
tags:
  - jekyll
  - github
---

GitHub Pages와 Jekyll을 사용하다보면 로컬 서버에서 사용할 때와 github pages에 배포된 상태를 구분하는 것이 필요가 있어, 그런 방법을 정리해보았다. 나는 보통 블로그 글을 작성하면 로컬 환경에서 jekyll을 돌리면서 보이는 화면을 확인하는 편인데, 그 때, google analytics가 잡히게 되면, 좀.. 나중에 통계를 볼 때 이상한 데이터가 너무 많이 들어오기 때문이다.

## 준비

그리고 나는 포스트의 레이아웃을 아래처럼 사용한다. (처음에 jekyll theme 중 하나를 끌어와서 사용했었기 때문에 내가 전부 작성한 코드는 아니고 일부를 수정한 코드들이다)

{% raw %}
```html
<html>
  ....
  ....
  <body>
    ....
    .... 수많은 콘텐츠.....
    ....

    {% include analytics.html %}
  </body>
</html>
```
{% endraw %}

`_includes/analytics.html`은 아래처럼 작성되어있다.

{% raw %}
```html
{% if site.google_analytics %}
	<!-- Google Analytics -->
	<script>
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

		ga('create', '{{ site.google_analytics }}', 'auto');
		ga('send', 'pageview', {
		  'page': '{{ site.baseurl }}{{ page.url }}',
		  'title': '{{ page.title | replace: "'", "\\'" }}'
		});
	</script>
	<!-- End Google Analytics -->
{% endif %}
```
{% endraw %}

위처럼 설정해두고 `_config.yml`에 `google_analytics: ~~~~` 와 같은 형식으로 설정해두면, 그 때부터 잘 트래킹이 된다.

## 문제점

하지만, 위처럼 사용할 경우, 로컬 서버를 구동시킬때에도, gh-pages에 배포가 되었을 때에도 트래킹이 된다. 즉, 로컬에서 내가 블로그에 글을 쓰면서 제대로 보이는지 확인하는 페이지 뷰까지도(정상적이지 않은 데이터) 계속해서 집계된다. 그래서 처음엔 귀찮아서 `_config.yml`에서 `google_analytics` 속성을 빼놓고 작성하게 되었지만, 자꾸 커밋할 때 신경이 쓰여서 고쳐보기로 했다.

## 해결법

그래서 로컬과 gh-pages 환경을 구분할 방법이 없을까 하다가 [Repository metadata on GitHub Pages](https://help.github.com/articles/repository-metadata-on-github-pages/)라는 문서를 찾게 되었다. 해당 문서는 GitHub Pages에 호스팅된 Jekyll 사이트에서 일반적인 레포지토리 정보들(프로젝트명, 설명 등등)을 받아올 수 있는 방법을 설명해준다. 해당 문서에서 `site.github` 네임스페이스를 사용한다고 설명을 하니, `site.github` 네임스페이스가 존재하는지 확인만 하면 간단히 구분이 가능하지 않을까 싶어서 시도해보았다.

{% include image.html url="/images/2019-02-17-jekyll/github.png" alt="site.github을 이용하자!" description="site.github을 이용하자!" class='noshadow' %}

즉, 아래처럼 코드를 수정해보고 잘 돌아가는지 확인해본후 배포해보았다.

{% raw %}
```html
{% if site.google_analytics and site.github %}
	<!-- Google Analytics -->
	<script>
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

		ga('create', '{{ site.google_analytics }}', 'auto');
		ga('send', 'pageview', {
		  'page': '{{ site.baseurl }}{{ page.url }}',
		  'title': '{{ page.title | replace: "'", "\\'" }}'
		});
	</script>
	<!-- End Google Analytics -->
{% endif %}
```
{% endraw %}

{% include image.html url="/images/2019-02-17-jekyll/commit.png" alt="이 부분만 고치면 로컬에서는 analytics가 뜨지 않는다." description="이 부분만 고치면 로컬에서는 analytics가 뜨지 않는다." class='noshadow' %}

결과는 예상했던 대로 잘 돌아간다.

{% include image.html url="/images/2019-02-17-jekyll/blog.png" alt="gh-pages에서는 성공적으로 트래킹이 된다." description="gh-pages에서는 성공적으로 트래킹이 된다." class='noshadow' %}

---

`site.github` 네임스페이스를 응용하면 몇몇 기능을 만들수도 있을 것 같긴 하지만, 귀찮아서 지금은 로컬 환경에서 disqus와 analytics를 끄는 용도로만 사용하고 있다.
