import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
# 우리가 만드는 단순한 설문조사(poll) 앱을 위해 Question 과 Choice 라는 두개의 모델을 만들어 보겠습니다.
# Question 은 질문(question) 과 발행일(publication date) 을 위한 두개의 필드를 가집니다.
# Choice 는 선택지(choice) 와 표(vote) 계산을 위한 두개의 필드를 가집니다. 각 Choice 모델은 Question 모델과 연관(associated) 됩니다.
# 이런 개념은 간단한 Python 클래스로 표현할 수 있습니다. polls/models.py 파일을 수정하여 다음과 같이 만들어 봅시다.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# 아주 간단한 코드입니다. 각 모델은 django.db.models.Model 이라는 클래스의 서브클래스로 표현됩니다.
# 각 모델은 몇개의 클래스 변수를 가지고 있으며, 각각의 클래스 변수들은 모델의 데이터베이스 필드를 나타냅니다.
# 데이터베이스의 각 필드는 Field 클래스의 인스턴스로서 표현됩니다.
# CharField 는 문자(character) 필드를 표현하고, DateTimeField 는 날짜와 시간(datetime) 필드를 표현합니다.
# 이것은 각 필드가 어떤 자료형을 가질 수 있는지를 Django 에게 말해줍니다.
# 각각의 Field 인스턴스의 이름(question_text 또는 pub_date)은 기계가 읽기 좋은 형식(machine-friendly format)의 데이터베이스 필드 이름입니다.
# 이 필드명을 Python 코드에서 사용할 수 있으며, 데이터베이스에서는 컬럼명으로 사용할 것입니다.
# Field 클래스의 생성자에 선택적인 첫번째 위치 인수를 전달하여 사람이 읽기 좋은(human-readable) 이름을 지정할 수도 있습니다.
# 이 방법은 Django 의 내부를 설명하는 용도로 종종 사용되는데, 이는 마치 문서가 늘어나는 것 같은 효과를 가집니다.
# 만약 이 선택적인 첫번째 위치 인수를 사용하지 않으면, Django 는 기계가 읽기 좋은 형식의 이름을 사용합니다.
# 이 예제에서는, Question.pub_date 에 한해서만 인간이 읽기 좋은 형태의 이름을 정의하겠습니다. 그 외의 다른 필드들은, 기계가 읽기 좋은 형태의 이름이라도 사람이 읽기에는 충분합니다.
# 몇몇 Field 클래스들은 필수 인수가 필요합니다. 예를 들어, CharField 의 경우 max_length 를 입력해 주어야 합니다.
# 이것은 데이터베이스 스키마에서만 필요한것이 아닌 값을 검증할때도 쓰이는데, 곧 보게 될것입니다.
# 또한 Field 는 다양한 선택적 인수들을 가질 수 있습니다. 이 예제에서는, default 로 하여금 votes 의 기본값을 0 으로 설정하였습니다.
# 마지막으로, ForeignKey 를 사용한 관계설정에 대해 설명하겠습니다. 이 예제에서는 각각의 Choice 가 하나의 Question 에 관계된다는 것을 Django 에게 알려줍니다.
# Django 는 다-대-일(many-to-one), 다-대-다(many-to-many), 일-대-일(one-to-one) 과 같은 모든 일반 데이터베이스의 관계들을 지원합니다.

# 모델에 대한 이 작은 코드가, Django에게는 상당한 양의 정보를 전달합니다. Django는 이 정보를 가지고 다음과 같은 일을 할 수 있습니다.
# > 이 앱을 위한 데이터베이스 스키마 생성(CREATE TABLE 문)
# > Question과 Choice 객체에 접근하기 위한 Python 데이터베이스 접근 API를 생성
# 그러나, 가장 먼저 현재 프로젝트에게 polls 앱이 설치되어 있다는 것을 알려야 합니다.
# 앱을 현재의 프로젝트에 포함시키기 위해서는, 앱의 구성 클래스에 대한 참조를 INSTALLED_APPS 설정에 추가해야 합니다.
# PollsConfig 클래스는 polls/apps.py 파일 내에 존재합니다. 따라서, 점으로 구분된 경로는 'polls.apps.PollsConfig'가 됩니다.
# 이 점으로 구분된 경로를, mysite/settings.py 파일을 편집하여 INSTALLED_APPS 설정에 추가하면 됩니다. 이는 다음과 같이 보일 것입니다.
# > mysite/settings.py로 가서 확인할 것.
