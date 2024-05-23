from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_employee and self.is_restaurant:
            raise ValidationError("User cannot be both employee and restaurant.")
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if Menu.objects.filter(restaurant=self.restaurant, day_of_week=self.day_of_week).exists():
            raise ValidationError("Menu for this day already exists for this restaurant.")
        super().save(*args, **kwargs)


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.BooleanField(default=False)
    voted_at = models.DateTimeField(auto_now_add=True)
