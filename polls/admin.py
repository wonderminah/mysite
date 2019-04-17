from django.contrib import admin
from .models import Question, Choice

# Register your models here.

# 관리 사이트에서 poll app 을 변경가능하도록 만들기¶
# 그런데, poll app 이 관리 인덱스 페이지에서 보이지 않네요. 어디에 있을까요?
# 여기서 하나만 더 하면 됩니다. 관리 사이트에 Question 객체가 관리 인터페이스를 가지고 있다는것을 알려주는 것입니다.
# 이것을 하기 위해서는, polls/admin.py 파일을 열어 다음과 같이 편집하면 됩니다.
admin.site.register(Question)
admin.site.register(Choice)
