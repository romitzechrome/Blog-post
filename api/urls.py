
from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('login', Login, basename="login")


urlpatterns = [
    path('', include(router.urls)),
    path('register/', Register.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(),
         name='user-retrieve-update-destroy'),
    path('blogpost/', PostListCreateView.as_view(), name='post-list-create'),
    path('blogupdatedelete/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(),
         name='post-retrieve-update-destroy'),
    path('likes/', LikesListCreateView.as_view(), name='likes-Send'),
    path('likesremove/', LikeRetrieveUpdateDestroyAPIViewDetailView.as_view(),
         name='likes-retrieve-update-destroy'),
]
