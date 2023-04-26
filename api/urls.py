
from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# this api for login user
router.register('login', Login, basename="login")


urlpatterns = [
#     route url
    path('', include(router.urls)),

#     this api for register user
    path('register/', Register.as_view()),

#     this api for retrive / update / delete user with authorization 
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(),
         name='user-retrieve-update-destroy'),

#     this api for create and get post details with like 
    path('blogpost/', PostListCreateView.as_view(), name='post-list-create'),

#     this api for update delete and retrive post data with like
    path('blogupdatedelete/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(),
         name='post-retrieve-update-destroy'),

#    this api for give a add like record like to post  
    path('likes/', LikesListCreateView.as_view(), name='likes-Send'),

#     this api for remove like and add like to post
    path('likesremove/', LikeRetrieveUpdateDestroyAPIViewDetailView.as_view(),
         name='likes-retrieve-update-destroy'),
]
