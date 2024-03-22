from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message,WealthUser

admin.site.register(WealthUser)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
