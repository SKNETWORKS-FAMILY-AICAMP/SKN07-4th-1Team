from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    content = models.TextField()