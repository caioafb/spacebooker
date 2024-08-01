from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    time_balance = models.IntegerField(default=720)
    space = models.ForeignKey("Space", null=True, blank=True, on_delete=models.CASCADE, related_name="space_users")

    def __str__(self):
        return self.username
    
    def is_admin(self):
        return self.space.admin == self

class Space(models.Model):
    name = models.CharField(max_length=30)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_spaces")

    def __str__(self):
        return self.name

class Booking(models.Model):
    day = models.DateField()
    time = models.TimeField()
    space = models.ForeignKey(User, on_delete=models.CASCADE, related_name="space_bookings")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="user_bookings")
    booker = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="booker_bookings")