from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('', views.success),
    path('login', views.login),
    path('logout', views.logout),
]
