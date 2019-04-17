from django.urls import path

from . import views

# 튜토리얼의 프로젝트는 polls라는 앱 하나만 가지고 진행했습니다. 실제 Django 프로젝트는 앱이 몇개라도 올 수 있습니다. Django는 이 앱들의 URL을 어떻게 구별해 낼까요?
# 예를 들어, polls 앱은 detail이라는 뷰를 가지고 있고, 동일한 프로젝트에 블로그를 위한 앱이 있을 수도 있습니다.
# Django가 {% url %} 템플릿태그를 사용할 때, 어떤 앱의 뷰에서 URL을 생성할지 알 수 있을까요?
# 정답은 URLconf에 이름공간(namespace)을 추가하는 것입니다. polls/urls.py 파일에 app_name을 추가하여 어플리케이션의 이름공간을 설정할 수 있습니다.
app_name = 'polls'

urlpatterns = [
    # 1
    # # /polls/
    # path('', views.index, name='index'),  # polls/urls.py > polls/views.py의 def index
    #
    # # /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    #
    # # /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    #
    # # /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),

    # 2
    # /polls/
    path('', views.IndexView.as_view(), name='index'),

    # /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    # /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]