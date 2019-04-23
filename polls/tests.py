import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
# 애플리케이션 테스트는 일반적으로 애플리케이션의 tests.py 파일에 있습니다. 테스트 시스템은 test 로 시작하는 파일에서 테스트를 자동으로 찾습니다.
# 우리는 미래의 pub_date를 가진 Question` 인스턴스를 생성하는 메소드를 가진 django.test.TestCase 하위 클래스를 생성했습니다.
# 그런 다음 was_published_recently()의 출력이 False가 되는지 확인했습니다.

# manage.py test polls는 polls 애플리케이션에서 테스트를 찾습니다.
# django.test.TestCase 클래스의 서브 클래스를 찾았습니다.
# 테스트 목적으로 특별한 데이터베이스를 만들었습니다.
# 테스트 메소드 - 이름이 test로 시작하는 것들을 찾습니다.
# test_was_published_recently_with_future_question에서 pub_date필드가 30일 미래인 Question 인스턴스를 생성했습니다
# ... assertIs() 메소드를 사용하여, 우리가 False가 반환되기를 원함에도 불구하고 was_published_recently() 가 True를 반환한다는 것을 발견했습니다.


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
# 이 중 일부를 더 자세히 살펴 보겠습니다.
# 먼저, 질문 생성 함수인 create_question은 테스트 과정 중 설문을 생성하는 부분에서 반복 사용합니다.
# test_no_questions는 질문을 생성하지는 않지만 "사용가능한 투표가 없습니다."라는 메시지 및 latest_question_list가 비어 있음을 확인합니다.
# django.test.TestCase 클래스는 몇 가지 추가적인 선언 메소드를 제공합니다. 이 예제에서 우리는 assertContains()와 assertQuerysetEqual()을 사용합니다.
# test_past_question에서 우리는 질문을 생성하고 그 질문이 리스트에 나타나는지 확인합니다.
# test_future_question에서 우리는 미래의 pub_date로 질문을 만듭니다.
# 데이터베이스는 각 테스트 메소드마다 재설정되므로 첫 번째 질문은 더 이상 존재하지 않으므로 다시 인덱스에 질문이 없어야 합니다.
# 요컨데, 사이트에서 관리자 입력 및 사용자 경험에 대한 이야기를 하는 테스트를 만들었고,
# 모든 상태와 시스템 상태의 모든 새로운 변경 사항에 대해 예상하는 결과가 출력되는지 확인합니다.


# 물론, 우리는 시간이 지난 pub_date 값을 가지고 있는 설문은 표시되고, 미래의 pub_date는 표시되지 않게 몇 가지 검사를 추가 할 것입니다.
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
