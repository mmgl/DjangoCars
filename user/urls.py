from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('password/', views.change_password, name='change_password'),
    path('update/', views.user_update, name='user_update'),

]