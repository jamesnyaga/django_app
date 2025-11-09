from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=100)
    header_image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('football', 'Football'),
            ('entertainment', 'Entertainment'),
            ('news', 'News'),
            ('education', 'Education'),
            ('tech', 'Tech'),
            ('others', 'Others'),
        ],
        default='others'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=False, blank=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description for the post")
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
        # Automatically create slug from title
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

            # Ensure slug is unique
            while Posts.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

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