from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
default_image = "http://"
default_dp = "http://"

DATA_TYPE = [
    ('txt', 'text'),
    ('img', 'image'),
    ('file', 'file'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(default=default_image)
    online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True)

class Room(models.Model):
    users = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)

class Group(models.Model):
    user = models.ManyToManyField(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    admin = models.ManyToManyField(User, related_name="group_admin")
    description = models.TextField(null=True, blank=True)
    dp = models.URLField(default=default_dp)


class Chats(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    typ = models.CharField(max_length=25, choices=DATA_TYPE, default='txt')
    text = models.TextField(null=True, blank=True)
    media = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)
    seen = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(User, related_name="chat_seen_by", blank=True)
    delivered = models.BooleanField(default=False)
    delivered_to = models.ManyToManyField(User, related_name="chat_delivered_to", blank=True)

class Friends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="user_friends")
    requests = models.ManyToManyField(User, blank=True, related_name="user_requests")
    requested = models.ManyToManyField(User, blank=True, related_name="user_requested")
    blocked = models.ManyToManyField(User, blank=True, related_name="user_blocked")

    # def update(self, *args, **kwargs):
    #     if hasattr(kwargs, 'friends'):
    #         self.friends 

