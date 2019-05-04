from django.urls import path, re_path

from . import views

app_name = 'data'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('analyze/', views.analyze_data, name='analyze'),
    path('detect/<str:lat>/<str:lon>/', views.detect, name='detect'),
]
