from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from django.utils import timezone


# Create your models here.
class Posts(models.Model):
	title = models.CharField(max_length=100)
	header_image = models.ImageField(null = True, blank=True, upload_to='blog_images/')
	content = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)
	image = models.ImageField(upload_to='post_images/', blank=True, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})



class Comment(models.Model):
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.body[:20]}'