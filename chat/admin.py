from django.contrib import admin
from .models import Profile, Room, Group, Chats, Friends

# Register your models here.
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Group)
admin.site.register(Chats)
admin.site.register(Friends)
