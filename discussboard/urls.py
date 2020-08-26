from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from .views import CommentLike


urlpatterns = [ # saying if you go to local host take you to the html page in the views.py file
    # http://127.0.0.1:8000
    # the home page at the moment
    path('', views.postList, name='posts'),
    path('post/newpost/', views.NewPost, name = 'newpost'),
    
    # http://127.0.0.1:8000/post/*the number its assigned*


    path('post/<int:pk>/', views.postDetail, name='postDetail'),
    path('post/<int:pk>/comment/', views.NewComment, name="newComment"),
    path('post/<int:pk>/like', views.CommentLike, name='commentLike'),
    path('post/<int:pk>/remove', views.commentRemove, name='commentRemove'),

    # http://127.0.0.1:8000/post/2/edit 
    path('post/<int:pk>/edit/', views.postEdit, name='postEdit'),
    path('post/<int:pk>/edit/delete/', views.RemovePost, name='removePost'),

    # http://127.0.0.1:8000/accounts/login/
    path('accounts/login/',  authViews.login_required, name = 'login'),

]