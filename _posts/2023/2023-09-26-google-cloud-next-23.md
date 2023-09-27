---
layout: post
title: "Google Cloud Next 23 Review"
tags:
    - conference
---

일부 회사를 통해 지원을 받아 Google Cloud Next 2023에 참가했고, 간단히 느낀 점을 정리해보려고 합니다.

## Google Cloud Next 2023

Google Cloud Next는 8월 29일부터 8월 31일까지 샌프란시스코 모스콘 센터에서 열렸습니다.
역시 GenAI 쪽 발표가 많았네요. 그와 더불어 연관된 데이터 베이스 세션도 많았습니다.
행사는 3일인데, 마지막 날은 많은 세션이 있진 않았고 오후 시간은 거의 마무리하는 시간이었습니다.

특히 좋았던 것은 같은 팀 분들이 많이 가다보니 많은 세션을 듣고 이야기를 나눌 수 있는 시간이었습니다.
앞 뒤로 같이 관광하던 것도 재밌었고요.

## 전반적인 행사

행사는 많이 유익했습니다.

{% include image.html url="/images/2023/gcn23/img1.jpeg" description="키노트!" %}

오픈소스 활동을 하면서 온라인으로만 만났던 분들도 만나고 궁금했던 내용도 많이 풀고 왔습니다.
서비스도 Vertex AI, 빅쿼리야 워낙에 잘 쓰고 있는데, GKE를 학습 용도로 쓰는 이유나 DB에서 이렇게 많은 서비스를 각자 만드는 이유,
어떤 것이 더 적합한지 등등 평소에 궁금한 내용과 세션을 들으며 궁금해지는 내용을 많이 들을 수 있었습니다.

하지만 역시 그 중에서 하는 일이 일이다 보니, GCP가 앞으로의 머신러닝 인프라에 대해 어떤 미래를 보고 어떤 해답을 제시하는지 명확하게 듣고 온 것이 좋았습니다.

Google Cloud 관련 분들만이 아닌, 고객사와 이야기해볼 수 있는 것도 좋았습니다.
예시로 스트리트 파이터를 만드는 Capcom 분들과 이야기해볼 시간이 있었는데,
Spanner를 왜 첫번째로 고려하고 가져갔는지 어떤 어려움이 있었는지 등에 대한 것을 들어볼 수 있는 것도 신기한 경험이었습니다.
보통은 한국쪽 고객사들, 미국쪽 고객사들 이야기만 들어왔는데 다양한 나라의 이야기를 듣는 것도 좋았습니다.

## 기억에 남는 내용들

개인적으로 ML 시대/Gen AI 시대의 소프트웨어 엔지니어에 관련된 내용으로 관심이 많았습니다.
듣고 이야기한 내용을 정리하면 아래 정도가 남는 것 같습니다.

ML 업계에서 일하는 사람으로서, 1) 모델 학습은 정말 필요한지 다시 고려하고 또 고려해야 한다.
왜 필요한지 잘 생각하자. 많은 제약사항이 존재하는 추천 등과 같은 분야를 제외하고 정말 필요할까.
1) 또, 당연하겠지만 LLM만이 해결책은 아니다. 오히려 잘 통합하는 것이 관건이다.
문제를 푸는 것에 집중할 수 있고, 이제는 머신러닝에 특화된 엔지니어와 그 여집합의 경계가 허물어지는 시대이다.

그럼 소프트웨어 엔지니어로서는?
1) 지금 변화하는 부분은 당장 적용이 가능한 것들로 인한 변화라고 느껴진다. 직업에 대한 관점이 바뀔 것이다.
특히 전반적인 엔지니어에 대한 기대가 굉장히 올라갈 것이다.
2) 그렇게 되면 가장 걱정되는 부분은 올라간 기대감에 대한 역량 검증이다. 생산성도 검증해야 한다.
3) 과연 모두가 잘 활용할 수 있을지? 같은 팀/조직/지역/국가 내에서 받아들이는 정도의 차이가 극심해진다면, 그에 대한 대처는 어떻게 해야할까.

대충 정리하면 이러한 내용인데, 많은 생각을 하고 왔고 유익했던 시간이었습니다.

제가 창업하면 과연 어떤 인프라를 쓸지 상상해보았는데 많은 부분을 단순하게 풀어낼 수 있을 것 같아 좋다고 생각이 드네요.