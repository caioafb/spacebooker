from django.contrib import admin

from .models import User, Space, Booking

admin.site.register(User)
admin.site.register(Space)
admin.site.register(Booking)