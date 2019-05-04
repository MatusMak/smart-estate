from django.urls import path, re_path

from . import views

app_name = 'data'

urlpatterns = [
    path('test/', views.test, name='test'),
]
