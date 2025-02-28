from django.urls import path
from .views import index

app_name = 'project4'
urlpatterns = [
    path('', views.index, name='index')
]
