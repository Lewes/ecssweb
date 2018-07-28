from django.db import models

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    message = models.TextField(verbose_name='Feedback')
    category = models.ForeignKey(Category, on_delete=models.SET('Others'), default=None)
    # Time when the feedback submitted
    time = models.DateField(auto_now_add=True)
    # Is the feedback submitted by people in ECS
    from_ecs = models.BooleanField(default=False)
    # Record if a committee member submitted the feedback
    committee = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.message

class Response(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Response')
    committee = models.CharField(max_length=150, null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class SubmittedIpRecord(models.Model):
    ip_hash = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
