from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(default=1, max_length=255, unique=True)

    def __str__(self):
        return str(self.category_name)


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = QuillField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='name')

    def preview(self):
        return f"{self.content[0:123]}..."

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        return reverse('notice-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Reply(models.Model):
    reply_content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='notice_replies')
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    accept = models.ManyToManyField(User, related_name='accepted')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "{}".format(self.commentator, self. notice)

    def get_absolute_url(self):
        return reverse('reply-detail', args=[str(self.id)])


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions')