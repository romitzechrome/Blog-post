from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class BlogPOST(models.Model):
    ID = models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    ID = models.AutoField(primary_key=True, null=False)
    post = models.ForeignKey(BlogPOST, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
