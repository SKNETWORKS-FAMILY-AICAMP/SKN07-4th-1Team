from django.urls import path
from .views import base_views, question_views


app_name = 'project4'
urlpatterns = [
    path('', base_views.index, name='index'),

    path('question/', question_views.question_view, name='question'),
]
