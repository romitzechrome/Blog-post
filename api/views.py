from django.contrib import messages
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .custompermission import *
from django.db.models import Q


class Register(APIView):

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            if user:
                json = {
                    'user': f' User registered Successfully...',
                    'status': status.HTTP_201_CREATED,
                }
            return Response(json)
        else:
            json = {
                'message': 'registration fail....',
                'status': 400,
            }
            return Response(json)


class Login(viewsets.ViewSet):

    def create(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            json = {
                'user': f'{username} login Successfully...',
                'token': str(token),
                "statu": status.HTTP_200_OK
            }
            return Response(json)
        else:
            return Response({'message': "Please enter valide Id Password", "status": status.HTTP_404_NOT_FOUND})


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        
        return User.objects.filter(id=self.request.user.id)


class PostListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = BlogPostSerializer

    def list(self, request):
        viewAllBlog = BlogPOST.objects.filter(
            Q(owner=self.request.user) | Q(is_public=True))
        list = []
        for i in viewAllBlog:
            list.append({
                "Id": i.ID,
                "title": i.title,
                "description": i.description,
                "content": i.content,
                "created_at": i.created_at,
                "owner": i.owner.username,
                "Is_Public": i.is_public,
                "Total_Like": len(Like.objects.filter(post=i.ID))
            })

        json_response = {"posts": list, "status": status.HTTP_200_OK}
        return Response(json_response)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        if self.request.method == "GET" :
            return BlogPOST.objects.filter(Q(owner=self.request.user) |Q(is_public=True))
        else:
            return BlogPOST.objects.filter(owner=self.request.user)

class LikesListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LikeBlogPostSerializer

    def list(self, request):
        likes = Like.objects.filter(user=self.request.user)
        list = []
        for i in likes:
            list.append({
                "ID": i.post.ID,
                "title": i.post.title,
                "description": i.post.description,
                "content": i.post.content,
                "created_at": i.post.created_at,
                "like by": i.user.username
            })

        json_response = {"posts": list, "status": status.HTTP_200_OK}
        return Response(json_response)


class LikeRetrieveUpdateDestroyAPIViewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeBlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        likeid = request.data['post']
        user = self.get_object()

        likeobj = Like.objects.filter(post=likeid, user=user.id)
        if likeobj:
            likeobj.delete()
            json = {
                'message': 'Remove like successfully.',
            }
            return Response(json)
        else:
            json = {
                'message': 'Some thing went wrong',
            }
            return Response(json)
