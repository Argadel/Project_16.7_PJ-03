from django import forms
from .models import Notice, Reply
from django.core.exceptions import ValidationError
from django_quill.forms import QuillFormField

class NoticeForm(forms.ModelForm):

    class Meta:
        model = Notice
        fields = ['title', 'content', 'category']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        name = cleaned_data.get("title")

        if name == content:
            raise ValidationError(
                "Content can not be the same as the title!"
            )

        return cleaned_data

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['reply_content', ]

