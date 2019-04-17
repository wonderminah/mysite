from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404


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


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)