
from django.db import models
from blog.models import Posts

class PostView(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} viewed at {self.viewed_at}"
