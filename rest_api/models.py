from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)


class Menu(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    items = models.JSONField()


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('menu', 'user')

