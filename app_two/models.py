from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Post(models.Model):
    title   = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    image   = models.ImageField(upload_to="Post_images/")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.PROTECT)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)




class Comment(models.Model):
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)



class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']


