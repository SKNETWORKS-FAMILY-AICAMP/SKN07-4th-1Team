from django.db import models


class Question(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

class SignUp(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content