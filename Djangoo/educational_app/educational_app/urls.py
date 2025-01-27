
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('slides/', views.slides_view, name='slides_view'),
    path('test/start/', views.start_test, name='start_test'),
    path('test/question/', views.test_question, name='test_question'),
    path('test/submit/', views.submit_answer, name='submit_answer'),
    path('test/result/', views.test_result, name='test_result'),
]
