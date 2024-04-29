from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from django.utils import timezone


# Create your models here.
class Posts(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})




"""class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'"""
  