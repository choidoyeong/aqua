from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(default = 0)

    class Meta:
        ordering = ('weight',)

class Water(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    liters = models.PositiveIntegerField(default=0)
    success = models.BooleanField(default=False)
    titration_liters = models.PositiveIntegerField(default=1500)
    
    class Meta:
        ordering = ['date']

class Tip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    class Mata:
        ordering = ['date']

    def __str__(self):
        return self.content

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']