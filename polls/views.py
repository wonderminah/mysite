from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse


# Create your views here.

# 뷰가 실제로 뭔가를 하도록 만들기¶
# 각 뷰는 두 가지 중 하나를 하도록 되어 있습니다. 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, 혹은 Http404 같은 예외를 발생하게 해야합니다. 나머지는 당신에게 달렸습니다.
# 당신이 작성한 뷰는 데이터베이스의 레코드를 읽을 수도 있습니다. 또한 뷰는 Django나 Python에서 서드파티로 제공되는 템플릿 시스템을 사용할 수도 있습니다.
# 뷰는 PDF를 생성하거나, XML을 출력하거나, 실시간으로 ZIP 파일을 만들 수 있습니다. 뷰는 당신이 원하는 무엇이든, Python의 어떤 라이브러리라도 사용할 수 있습니다.
# Django에 필요한 것은 HttpResponse 객체 혹은 예외입니다.
# 왜냐면, 그렇게 다루는게 편리하기 때문입니다. 튜토리얼 2장의 예제에서 다룬 Django 자체 데이터베이스 API를 사용해봅시다.
# 새로운 index() 뷰 하나를 호출했을 때, 시스템에 저장된 최소한 5 개의 투표 질문이 콤마로 분리되어, 발행일에 따라 출력됩니다.

def index(request):
    # 1
    # return HttpResponse("Hello, world. You're at the polls index.")

    # 2
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 3
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {'latest_question_list': latest_question_list}
    # return HttpResponse(template.render(context, request))

    # 4
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # 1
    # return HttpResponse("You're looking at question %s" % question_id)

    # 2: 이제, 질문의 상세 뷰에 태클을 걸어보겠습니다. 상세 뷰는 지정된 설문조사의 질문 내용을 보여줍니다. 다음과 같습니다.
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Questions does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    # 3: 지름길: get_object_or_404()
    # 만약 객체가 존재하지 않을 때 get() 을 사용하여 Http404 예외를 발생시키는것은 자주 쓰이는 용법입니다.
    # Django에서 이 기능에 대한 단축 기능을 제공합니다. detail() 뷰를 단축 기능으로 작성하면 다음과 같습니다.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    # 2번에서는 에러미시지를 지정할 수 있었지만, 여기서는 지정이 없기 때문에 실행 결과 "No Question matches the given query."이라는 에러 메시지가 출력된다.
    # 상위 계층에서 ObjectDoesNotExist 예외를 자동으로 잡아 내는 대신
    # get_object_or_404() 도움 함수(helper functoin)를 사용하거나, ObjectDoesNotExist 예외를 사용하는 대신 Http404 를 사용하는 이유는 무엇일까요?
    # 왜냐하면, 모델 계층을 뷰 계층에 연결하는 방법이기 때문입니다.
    # Django의 중요한 설계 목표는, 약결합(loose coupling)을 관리하는 데에 있습니다. 일부 제어된 결합이 django.shortcuts 모듈에서 도입되었습니다.


def results(request, question_id):
    # return HttpResponse("You're looking at the results of question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # 위 코드는 이 튜토리얼에서 아직 다루지 않은 몇 가지를 포함하고 있습니다:
    # request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체입니다.
    # 이 경우, request.POST['choice'] 는 선택된 설문의 ID를 문자열로 반환합니다. request.POST 의 값은 항상 문자열들입니다.
    # Django는 같은 방법으로 GET 자료에 접근하기 위해 request.GET 를 제공합니다
    # -- 그러나 POST 요청을 통해서만 자료가 수정되게하기 위해서, 명시적으로 코드에 request.POST 를 사용하고 있습니다.
    # 만약 POST 자료에 choice 가 없으면, request.POST['choice'] 는 KeyError 가 일어납니다.
    # 위의 코드는 KeyError 를 체크하고, choice가 주어지지 않은 경우에는 에러 메시지와 함께 설문조사 폼을 다시보여줍니다.
    # 설문지의 수가 증가한 이후에, 코드는 일반 HttpResponse 가 아닌 HttpResponseRedirect 를 반환하고, HttpResponseRedirect 는 하나의 인수를 받습니다
    # :그 인수는 사용자가 재전송될 URL 입니다. (이 경우에 우리가 URL을 어떻게 구성하는지 다음 항목을 보세요).
    # 위의 파이썬 주석이 지적했듯이, POST 데이터를 성공적으로 처리 한 후에는 항상 HttpResponseRedirect 를 반환해야합니다.
    # 이 팁은 Django에만 국한되는것이 아닌 웹개발의 권장사항입니다.
    # 우리는 이 예제에서 HttpResponseRedirect 생성자 안에서 reverse() 함수를 사용하고 있습니다.
    # 이 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와줍니다.
    # 제어를 전달하기 원하는 뷰의 이름을, URL패턴의 변수부분을 조합해서 해당 뷰를 가리킵니다
    # 여기서 우리는 튜토리얼 3장에서 설정했던 URLconf를 사용하였으며, 이 reverse() 호출은 아래와 같은 문자열을 반환할 것입니다.
    # '/polls/3/results/'
    # 여기서 3 은 question.id 값입니다. 이렇게 리디렉션된 URL은 최종 페이지를 표시하기 위해 'results' 뷰를 호출합니다.
