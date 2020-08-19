from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('password/', views.change_password, name='change_password'),
    path('update/', views.user_update, name='user_update'),
    path('comments/', views.comments, name='comments'),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    path('add_content/', views.add_content, name='add_content'),

]