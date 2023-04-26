from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="A user with that email address already exists.")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password']

        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        username = validated_data['username']
        password = validated_data['password']
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPOST
        fields = ['ID', 'title', 'description', 'content',
                  'created_at', 'is_public']

        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'content': {'required': True},
            'is_public': {'required': True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        blogpost = BlogPOST()
        blogpost.owner = User.objects.get(id=request.user.id)
        blogpost.title = validated_data['title']
        blogpost.description = validated_data['description']
        blogpost.content = validated_data['content']
        blogpost.is_public = validated_data['is_public']
        blogpost.save()
        return blogpost


class LikeBlogPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['post']

        extra_kwargs = {
            'post': {'required': True},
        }

    def validate(self, data):
        request = self.context.get("request")
        likeforpost = Like.objects.filter(
            user=request.user.id, post=data['post'].ID)
        if len(likeforpost) == 0:
            checkpublic = BlogPOST.objects.get(ID=data['post'].ID)
            if checkpublic.is_public == False and checkpublic.owner.id != request.user.id:
                raise serializers.ValidationError({
                    "message": f"You don't have authority to like this post : {data['post'].title}."
                })

            return data
        else:
            raise serializers.ValidationError({
                "message": f"Already Like This post : {data['post'].title}."
            })

    def create(self, validated_data):
        request = self.context.get("request")
        likeobj = Like()
        likeobj.user = User.objects.get(id=request.user.id)
        likeobj.post = BlogPOST.objects.get(ID=validated_data['post'].ID)
        likeobj.save()
        return likeobj
