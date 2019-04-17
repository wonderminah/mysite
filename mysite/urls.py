"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    # mysite/urls.py > polls/urls.py
    # include() 함수는 다른 URLconf들을 참조할 수 있도록 도와줍니다.
    # Django가 함수 include()를 만나게 되면, URL의 그 시점까지 일치하는 부분을 잘라내고,
    # 남은 문자열 부분을 후속 처리를 위해 include 된 URLconf로 전달합니다.
    # https://docs.djangoproject.com/ko/2.2/intro/tutorial01/
    # 언제 include()를 사용해야 하나요? > 다른 URL 패턴을 포함할 때마다 항상 include()를 사용해야 합니다. admin.site.urls가 유일한 예외입니다.
]
