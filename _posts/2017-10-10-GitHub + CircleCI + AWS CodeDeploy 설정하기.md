---
layout: post
title: "GitHub + CircleCI + AWS CodeDeploy 설정하기"
tags:
  - ci
  - devops
  - aws
---

 저는 GitHub Developer Plan (Unlimited private repos가 가능한 Plan)을 사용하는 만큼, 소스코드 저장을 할 때 GitHub 레포지토리를 많이 사용을 합니다. 그래서 가끔 간단한 일을 할 때에 GitHub와 CircleCI를 연동하여 빌드/테스트를 진행했었고, 필요하다면 AWS의 CodeDeploy를 이용하여 자동으로 배포를 진행하였습니다. 오늘은 그 방법에 대해서 써보도록 하겠습니다.
 
 **한가지 주의**를 당부드리자면, 배워가는 과정에서 쓴 글이기 때문에 부정확한 정보와 비효율적인 방법이 담겨있을 수 있습니다. 그 부분에 대해서는 어느정도 생각을 하시고 읽어주셨으면 합니다.
 
## GitHub
 
### GitHub 설정
 
 GitHub에서는 `appspec` 파일을 포함한 하나의 새로운 레포지토리를 준비하면 됩니다.
 
![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/github-new-repository.png)

`appspec` 파일이란 무엇일까요?

### AppSpec File

[AWS CodeDeploy User Guide](http://docs.aws.amazon.com/codedeploy/latest/userguide/application-specification-files.html)에는 이렇게 나와 있습니다

> An application specification file (AppSpec file), which is unique to AWS CodeDeploy, is a YAML-formatted file used to:
>
> * Map the source files in your application revision to their destinations on the instance.
> * Specify custom permissions for deployed files.
> * Specify scripts to be run on each instance at various stages of the deployment process.
> 
> The AppSpec file is used to manage each deployment as a series of lifecycle events. Lifecycle event hooks, which are defined in the file, allow you to run scripts on an instance after many of the individual deployment lifecycle events. AWS CodeDeploy runs only those scripts specified in the file, but those scripts can call other scripts on the instance. You can run any type of script as long as it is supported by the operating system running on the instances.
 
 AppSpec 파일은 Application Specification File이고, YAML 포맷의 파일이다. 이 파일은 Instance상의 특정 목적 디렉토리로 소스 파일들을 매핑해주고, 배포 파일들의 퍼미션을 설정해주며, Deployment Process 주기 중 실행되어야 할 스크립트들을 정해준다. 즉, 각 배포에 해당하는 생명주기를 관리하기 위한 파일이다.

 이 정도로 이해하시면 될 것 같습니다.
 
 그 `appspec`을 작성하는 방법은 [AWS CodeDeploy AppSpec File Reference](http://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file.html)에 잘 나와 있습니다. 짤막하게 설명을 해보자면, 
 
```yaml
version: 0.0
os: operating-system-name
files:
  source-destination-files-mappings
permissions:
  permissions-specifications
hooks:
  deployment-lifecycle-event-mappings
```

 위와 같은 구조를 가집니다. 파일 구조를 보시면 이해하시겠지만, 맨 처음 설명했던 파일 매핑, 퍼미션, 생명주기 관리는 파일 구조상의 세가지 섹션에 해당하는 부분입니다. ```version```은 고정되는 섹션이고, ```os```는 ```linux```또는 ```windows```의 값을 가집니다.
 
 그 후 자세한 부분은 Reference를 참고하시면 이해가 잘 가실 겁니다.
 
```yaml
version: 0.0
os: linux
files:
  - source: Config/config.txt
    destination: /webapps/Config
  - source: source
    destination: /webapps/myApp
hooks:
  BeforeInstall:
    - location: Scripts/UnzipResourceBundle.sh
    - location: Scripts/UnzipDataBundle.sh
  AfterInstall:
    - location: Scripts/RunResourceTests.sh
      timeout: 180
  ApplicationStart:
    - location: Scripts/RunFunctionalTests.sh
      timeout: 3600
  ValidateService:
    - location: Scripts/MonitorService.sh
      timeout: 3600
      runas: codedeployuser
```

위는 AWS User Guide에서 소개하는 `appspec`파일 예제입니다. 리눅스 인스턴스 상에서 필요한 파일들을 매핑시키고, `BeforeInstall`, `AfterInstall`과 같은 생명주기를 이용하여 스크립트를 실행시킵니다.

참고로 `appspec.yml`파일은 레포지토리 루트 디렉토리에 위치합니다.

GitHub 내에서 그 외에 필요한 설정은 circleci와 관련된 설정 정도입니다.

## CircleCI

### CircleCI가 무엇일까

CI 서버를 따로 구축하지 않아도 되도록 [GitHub Marketplace](https://github.com/marketplace)에서 다양한 Continuous integration을 지원합니다. 그 중 하나인 CircleCI입니다.

![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/github-marketplace.png)

CircleCI는 private repo든, public repo든 container 1개를 지원합니다. 여러 개의 컨테이너가 필요한 작업이 저는 많이 없기 때문에 Free Plan을 이용해서 했습니다. (데이터 베이스가 필요한 경우가 물론 있지만, 그런 경우는 따로 테스트 데이터 베이스를 외부로 빼서 씁니다.)

![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/circleci-plans.png)

CircleCI Setup을 하고 나면, 여러가지 project들을 Setup할 수 있도록 나오는데, 필요한 레포지토리를 Setup project 버튼을 눌러줍니다.

그 후 레포지토리 내에 circleci 설정파일을 추가해서 push를 날리면 알아서 설정 파일 내에 명시된 대로 빌드를 진행해줍니다.

### circleci 설정

circleci 설정 파일은 사용하시는 언어에 따라서 미리 어느정도 가이드가 작성되어 있기 때문에 그 가이드를 참고하시면 될 것 같습니다.

![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/circleci-python-tutorial.png)

* [CircleCI Language Guide: Python](https://circleci.com/docs/2.0/language-python/)
* [CircleCI Language Guide: Ruby](https://circleci.com/docs/2.0/language-ruby/)
* [CircleCI Language Guide: Android](https://circleci.com/docs/2.0/language-android/)

위와 같은 경우를 제외하고도 Clojure, Elixir, Go, Java, JavaScript, PHP 같은 언어를 기본적으로 가이드를 작성해놓고 있습니다.

저는 Python을 기본적으로 많이 이용하는만큼, [Django Demo Project](https://github.com/CircleCI-Public/circleci-demo-python-django)의 [설정 파일](https://github.com/CircleCI-Public/circleci-demo-python-django/blob/master/.circleci/config.yml)을 고쳐서 쓰고 있습니다.

circleci 설정파일의 경로는 레포지토리의 `.circleci/config.yml` 파일입니다. 자세한 파일 레퍼런스는 다음 링크를 참고하시면 될 것 같습니다.

* [CircleCI 2.0 Documentation](https://circleci.com/docs/2.0/)

참고로 저는 아래와 같은 형식으로 설정 파일을 사용하고 있습니다.

{% raw %}
```yaml
version: 2
jobs:
  build:
    docker:
      - image: circleci/python:3.6.1

    working_directory: ~/project-name

    steps:
      - checkout
      
      - restore_cache:
          keys:
          - deps-{{ .Branch }}-{{ checksum "requirements.txt" }}

      - run:
          name: install dependencies
          command: |
            python3 -m venv env
            . env/bin/activate
            pip install -r requirements.txt
            pip install awscli --upgrade

      - save_cache:
          paths:
            - ./env
          key: deps-{{ .Branch }}-{{ checksum "requirements.txt" }}
        
      - run:
          name: run tests
          command: |
            . env/bin/activate
            python setup.py test


      - deploy:
          name: AWS Deployment
          command: |
            if [ "${CIRCLE_BRANCH}" == "release" ]; then
              ./env/bin/aws deploy create-deployment --application-name application-name --deployment-group-name deployment-group-name --region aws-region --github-location repository=username/reponame,commitId=$CIRCLE_SHA1
            fi
```
{% endraw %}

짤막한 설명을 적어보자면, 도커 컨테이너는 Python 3.6.1 버전을 사용하고, 빌드 과정은 checkout(프로젝트의 소스코드를 받아옴) 후, 저장되어 있는 cache를 받아옵니다. 그 후 dependencies를 설치하고, 해당 dependencies를 저장합니다. 그리고 미리 작성한 unittest를 실행하고 aws deploy를 실행합니다.

deploy 부분의 if문은 푸쉬된 브랜치가 release인지 체크하는 브랜치입니다. 저 부분 브랜치별로 다르게 배포하도록 더 추가하셔도 되고, 브랜치 명을 바꾸셔도 됩니다.

aws deployment와 관련된 부분은 awscli를 사용한 것이기 때문에 [AWS 명령줄 인터페이스](https://aws.amazon.com/ko/cli/)를 참고하시면 될 것 같습니다. 또한 이 부분에 대해서는 다음 섹션에 나오는 AWS CodeDeploy 설정과 연결되는 부분이기 때문에 다음 섹션을 읽고 다시 작성하시는 것이 좋을 것 같습니다.

## AWS CodeDeploy

### AWS CodeDeploy에 대해

AWS 홈페이지에서는 AWS CodeDeploy에 대해서 이렇게 설명하고 있습니다. [해당 페이지 링크](https://aws.amazon.com/ko/codedeploy/)

> AWS CodeDeploy는 Amazon EC2 인스턴스 및 온프레미스에서 실행 중인 인스턴스를 비롯한 모든 인스턴스에 대한 코드 배포를 자동화하는 서비스입니다. AWS CodeDeploy를 사용하면 새로운 기능을 더욱 쉽고 빠르게 출시할 수 있고, 애플리케이션을 배포하는 동안 가동 중지 시간을 줄이는 데 도움이 되며, 복잡한 애플리케이션 업데이트 작업을 처리할 수 있습니다. AWS CodeDeploy로 소프트웨어 배포를 자동화하면 오류가 발생하기 쉬운 수동 작업을 할 필요가 없어지고 인프라에 따라 서비스가 확장되므로 하나 또는 수천 개의 인스턴스에 손쉽게 배포할 수 있습니다.

 서비스 명에서 쉽게 유추할 수 있듯 코드 배포를 도와주는 자동화 도구입니다. 여러가지 배포방식을 지원하며, 그룹을 나눌 수 있어 매우 유용한 도구입니다. 또한 언어에 구애받지 않는 도구이기 때문에 자유로운 방식의 배포 도구입니다.

### IAM

우선, 우린 IAM이란 것을 설정해야 합니다. IAM은 Identity and Access Management의 약어입니다. 계정 권한을 관리하는 그런 서비스를 말합니다. IAM은 다음 링크로 들어가면 접속할 수 있습니다.

* [AWS IAM](https://console.aws.amazon.com/iam/home)

IAM에서 Role 2개, User 하나를 추가하시면 됩니다.

### IAM Role

추가해야 할 IAM Role은 다음 두가지입니다.

* EC2 인스턴스에 정해줄 IAM Role
* CodeDeploy Application에 정해줄 IAM Role

EC2 인스턴스에 정해줄 IAM Role을 편의상 `EC2CodeDeploySample`이라고 부르겠습니다. 그리고 CodeDeploy Application에 정해줄 IAM Role은 편의상 `CodeDeploySample`이라고 부르겠습니다. 

먼저 `CodeDeploySample` Role을 만들어줍니다. 해당 Role에 설정해줄 것은 두 가지입니다.

첫째로, Trust Relationship을 설정해주는 것입니다. 이 것은 다음과 같이 설정해줍니다. 설정 파일 안의 region 부분은 적당히 수정해주시기 바랍니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "codedeploy.ap-northeast-2.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

이렇게 설정을 한다면 다음과 같이 나타납니다.

Trusted entities

* The identity provider(s) **ec2.amazonaws.com**
* The identity provider(s) **codedeploy.ap-northeast-2.amazonaws.com**

둘째로, Policy를 설정해주어야 합니다. 이 부분은 Inline Policy로 만들어서 직접 작성하시는 것이 편할 겁니다.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "autoscaling:PutLifecycleHook",
                "autoscaling:DeleteLifecycleHook",
                "autoscaling:RecordLifecycleActionHeartbeat",
                "autoscaling:CompleteLifecycleAction",
                "autoscaling:DescribeLifecycleHooks",
                "autoscaling:DescribeAutoscalingGroups",
                "autoscaling:PutInstanceInStandby",
                "autoscaling:PutInstanceInService",
                "ec2:Describe*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

autoscaling과 관련되어서 "어라? 난 autoscaling 그룹 지정안할건데?"라고 생각하시는 분이 있을 수 있는데, CodeDeploy 설정하는 부분에서 막혀서 실행이 되지 않는 것이 존재합니다. 물론 하나하나 다 테스트 해본 것이 아니기 때문에 더 자세한 정보를 알려주신다면 수정토록 하겠습니다.

그 다음 `EC2CodeDeploySample`을 설정합니다. 이 Role에도 설정해줄 것은 두 가지입니다.

Trust Relationship은 다음과 같이 설정해줍니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

ec2 서비스만 등록합니다.

Policy는 다음과 같이 설정합니다. Inline Policy를 통해 직접 작성하시는 것이 편할 수 있습니다.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

이 부분의 policy는 왜 저렇게 설정하는지 잘 이해가 가지 않습니다. 아마도 s3에서 소스를 가져오는 옵션이 존재하기 때문인 것 같습니다.

### IAM User

이제 IAM User를 설정해줄 차례입니다.

이 User는 Access Key를 생성하여 aws cli에서 이용하기 위해 만듭니다. 만들 때 programmatic access라는 옵션에 체크해주시고, policy는 `AWSCodeDeployFullAccess`를 하나 추가해주시면 됩니다.

여기서 만들어주는 Secret Key 두 개를 잘 보관해주시기 바랍니다.

### EC2 Instance

EC2 Instance는 어떻게 만드셔도 큰 상관은 없지만, 저는 Amazon Linux를 기준으로 작성하겠습니다. 

EC2 Instance를 생성하면서 IAM 역할을 `EC2CodeDeploySample`로 정해서 EC2 Instance를 생성해줍니다. 그 후 ssh로 접속하여 codedeploy-agent를 설치해주는데, 그 방법은 다음과 같습니다.

```shell
$ sudo yum update
$ sudo yum install ruby
$ sudo yum install wget
$ cd /home/ec2-user
$ wget https://bucket-name.s3.amazonaws.com/latest/install
$ chmod +x ./install
$ sudo ./install auto
```

중간에 bucket-name은 저희가 입력해주어야 하는 부분인데, 다음링크로 들어가시면 확인하실 수 있습니다. [리전별 리소스 키트 버킷 이름](http://docs.aws.amazon.com/ko_kr/codedeploy/latest/userguide/resource-kit.html#resource-kit-bucket-names). 참고로 서울지역의 bucket-name은 `aws-codedeploy-ap-northeast-2`입니다.

위처럼 설치하신 후 서비스가 구동중인지 확인하셔야 합니다.

```shell
$ sudo service codedeploy-agent status
$ # 만약 구동중이 아니라면
$ sudo service codedeploy-agent start
```

더 자세한 설명은 [AWS CodeDeploy 에이전트 설치 또는 다시 설치](http://docs.aws.amazon.com/ko_kr/codedeploy/latest/userguide/codedeploy-agent-operations-install.html)에 나와있습니다.

### CodeDeploy 설정

이제 드디어 CodeDeploy 설정으로 왔습니다.

CodeDeploy 설정은 나머지 부분은 적당히 원하는 배포방식에 맞추어 하시면 됩니다. EC2 Instance도 태그로 설정하시면 됩니다. 다만, **서비스 역할 ARN** 부분은 앞서 설정했던 `CodeDeploySample`로 설정하셔야 합니다. 

그리고 "AWS CodeDeploy - 배포"로 접속하신 후 GitHub 계정과 연결하기 위해 초기 배포를 진행해줍니다.

배포 만들기를 눌러준 후 다음과 같이 설정해줍니다.

![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/code-deploy.png)

리포지토리 유형을 GitHub로 설정하시고, GitHub 계정을 연결하신 후 리포지토리 이름(UserName/RepoName 형식)으로 작성하시고, 커밋 ID(SHA1)을 입력해주시면 됩니다. 기타 롤백등 나머지 옵션은 필요하신 대로 하시면 됩니다.

만약 배포가 성공적으로 된다면 이제 CircleCI의 IAM User 설정을 통해 시도해봅니다.

### 다시 CircleCI로

CircleCI의 Project Settings에는 Permissions 섹션에 AWS Permissions 란이 존재합니다. 해당 AWS Permissions에 IAM User를 발급하고 받은 Access Key를 입력해줍니다.

![]({{ site.url }}/images/2017-10-10-github-aws-codedeploy/aws-permission.png)

그리고 앞서 작성한 `.circleci/config.yml` 중 deploy 부분의 command 란의 옵션을 수정해줍니다. (`--application-name application-name --deployment-group-name deployment-group-name --region aws-region --github-location repository=username/reponame,commitId=$CIRCLE_SHA1` 부분)

## 끝

이제 모든 설정이 끝났습니다. 테스트로 awscli 명령어를 바로 작성해보거나, 테스트 코드를 작성한 후 GitHub repo에 푸쉬해보시기 바랍니다.
