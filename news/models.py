from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(News.Status.PUBLISHED)
class News(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft',
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    view =models.PositiveIntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_posts')
    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.id])

    def increase_view(self):
        self.view += 1
        self.save()
from taggit.managers import TaggableManager
class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True)
    content = models.TextField()
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f'Comments by {self.name} on {self.post}'