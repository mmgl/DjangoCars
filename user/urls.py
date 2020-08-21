from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('password/', views.change_password, name='change_password'),
    path('update/', views.user_update, name='user_update'),
    path('comments/', views.comments, name='user_comments'),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),

    path('addcontent/', views.addcontent, name='addcontent'),
    path('contents/', views.contents, name='contents'),
    path('contentedit/<int:id>', views.contentedit, name='contentedit'),
    path('contentsdelete/<int:id>', views.contentdelete, name='contentdelete'),

]