from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app/', views.app, name='app'),
    path('email/', views.email, name='email'),
    path('select/', views.select, name = 'select')
]