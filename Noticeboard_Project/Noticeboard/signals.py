from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notice, Reply, User
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Notice)
def create_email_for_notice_author(sender, instance, created, **kwargs):
   if created:
       if not created:
           return

       emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)

       subject = f'New notice in {instance.category}!'

       text_content = (
           f'Title: {instance.title}\n'
           f'Check it out now: http://127.0.0.1:8000{instance.get_absolute_url()}'
       )
       html_content = (
           f'Title: {instance.title}<br>'
           f'Check it out now: http://127.0.0.1:8000{instance.get_absolute_url()}'
       )
       for email in emails:
           msg = EmailMultiAlternatives(subject, text_content, None, [email])
           msg.attach_alternative(html_content, "text/html")
           msg.send()


@receiver(post_save, sender=Reply)
def create_email_for_notice_author(sender, instance, created, **kwargs):
   if created:
       notice = instance.notice
       author = notice.author

       subject = 'New reply!'
       text = f'{author.username}, you have just received a new reply! Check it out on our website - My Noticeboard!'
       html = (
           f'{author.username}, you have just received a new reply! '
           f'Check it out on our website - <a href="http://127.0.0.1:8000/">My Noticeboard</a>!'
       )
       msg = EmailMultiAlternatives(
           subject=subject, body=text, from_email=None, to=[author.email]
       )
       msg.attach_alternative(html, "text/html")
       msg.send()
