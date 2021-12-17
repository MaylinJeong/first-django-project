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
