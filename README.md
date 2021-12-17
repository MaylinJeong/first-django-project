# first-django-project

Django Practice Following [Django Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)

## Tutorial 1

- Creating a project
  - ```
    $ django-admin startproject <project-name>
    ```
- Project Directory
  - ```commandline
    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py
    ```
  
## Tutorial 2

[Accessing related objects](https://docs.djangoproject.com/en/4.0/ref/models/relations/)

- 1:N Relation
  - FK로 relation 을 가지는 모델은, 하위 모델을 `<sub-model name>_set` 으로 접근하는 것 같다
  ```commandline
  # Display any choices from the related object set -- none so far.
  >>> q.choice_set.all()
  <QuerySet []>
  
  # Create three choices.
  >>> q.choice_set.create(choice_text='Not much', votes=0)
  <Choice: Not much>
  >>> q.choice_set.create(choice_text='The sky', votes=0)
  <Choice: The sky>
  ```

  - 하위 relation의 objects 는 related 된 object 에 접근이 가능하다.
    ```commandline
    >>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
    # Choice objects have API access to their related Question objects.
    >>> c.question
    <Question: What's up?>
    ```
  
  - Use double underscores to separate relationships
    ```commandline
    >>> Choice.objects.filter(question__pub_date__year=current_year)
    # question : object, pub_date : field, year : date_time
    <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
    ```
    double underscore 로 다른 테이블과의 join 이 가능하며, 내 테이블의 필드 접근도 가능하다.
    for details.. [Field lookups](https://docs.djangoproject.com/en/4.0/topics/db/queries/#field-lookups-intro)

- Django Admin
  - 컨셉은 "content publishers" 와 "public" 을 분리하는 것
  - Create an admin user
    ```commandline
    $ python manage.py createsuperuser
    ```
  - groups and users provided by `django.contrib.auth` (authentication framework)
    - for Details... [User authentication in Django](https://docs.djangoproject.com/en/4.0/topics/auth/#module-django.contrib.auth)
  - Question objects 를 admin 에 추가하려면, admin.py dp Question을 등록하면 된다.
    ```commandline
    from django.contrib import admin
  
    from .models import Question
  
    admin.site.register(Question)
    ```
    - `admin.site.register(Question)` 은 어디서 나온 코드인지 따라가 봤다.
    - /.venv/lib/python3.10/site-packages/django/contrib/admin
      - 이 경로에 sites.py 가 있고, `register` 메서드를 제공한다.

## Tutorial3

will focus on creating the public interface – “views.”
To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.
- for details.. [URL dispatcher](https://docs.djangoproject.com/en/4.0/topics/http/urls/)

- 어떻게 URL을 해석하는지
  - 먼저, `mysite.urls` 로 가서 url pattern 을 찾는다.
  - 찾았다면, 해당 url에 remaning text 를 전달한다.
- `views.py` 는 controller 역할을 한다 
  ```python
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      output = ', '.join([q.question_text for q in latest_question_list])
      return HttpResponse(output)
  ```
- The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True. 이렇게 설정되어 있으면, <app 이름>/templates/ 아래부터 searching 하게된다.
  - 따라서, polls/templates/polls/index.html 일 경우, polls/index.html 로 접근할 수 있게 된다.
  - 추후 여러 templates 를 생성하게 되니까, 이렇게 naming 하는 것이 바람직하다.
    > We need to be able to point Django at the right one, and the best way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

- html 에서 url 접근하는 방법
  - 하드 코딩하지 말고, polls/urls.py 에서 path() function을 기입하면, html 에서 `{% url %}` 로 접근가능하다
    ```python
    urlpatterns = [
        path('', views.index, name='index'),
        # /polls/5
        path('<int:question_id>/', views.detail, name="detail"),
        # /polls/5/results/
        path('<int:question_id>/results/', views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
    ```
    
  
## Tutorial4

will focus on form processing and cutting down our code

- CQRS 보안 이슈를 방지하기 위해 `{% csrf_token %}` 를 쓰면 Django에서 자동으로 protect 해준다.
- `reverse`
  - If you need to use something similar to the url template tag in your code, Django provides the following function: `reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)`
  - `urls.py` 에 명시되어 있는 path() 를 사용해서 url 를 하드코딩 하지 않아도 된다.
- 현재 tutorial 버전으로는 vote 의 count를 계산하는 데 race condition 이 생긴다.
  - for details.. [Avoiding race conditions using F()](https://docs.djangoproject.com/en/4.0/ref/models/expressions/#avoiding-race-conditions-using-f)
