from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Room, Topic, Message,WealthUser

class WealthUserAdmin(UserAdmin):
    pass 

admin.site.register(WealthUser,WealthUserAdmin)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
