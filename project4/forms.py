from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']
        labels = {
            'content': '질문내용'
        }
        