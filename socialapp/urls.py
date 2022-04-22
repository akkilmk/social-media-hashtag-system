
from . import views
from django.urls import  path

urlpatterns = [
    path('',views.SignUp.as_view(),name="signup"),
    path('login/',views.LogIn.as_view(),name="login"),
    path('createpost/',views.CreatePost.as_view(),name='createpost'),
    path('trending/',views.Trending.as_view(),name ='trending'),
    path('serachhashtag/',views.SerachHashtag.as_view(),name='searching')
]
