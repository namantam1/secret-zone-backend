from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Room, User, Chats

from django.utils.timezone import localtime
from django.utils.timesince import timesince
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class JsTimestampField(serializers.Field):
    def to_representation(self, value):
        return round(value.timestamp()*1000)


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    lastSeen = JsTimestampField(source='profile.last_seen')
    online = serializers.SerializerMethodField()
    def get_online(self, obj):
        return obj.profile.online

    def get_image(self, obj):
        return obj.profile.image

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'image', 'lastSeen', 'online']

class UserLoginSerializer(TokenObtainPairSerializer):

    default_error_messages = {
        'no_active_account': _('Invalid username or password.')
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class ChatSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False)
    chatId = serializers.IntegerField(source='id', required=False)
    roomId = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room')
    # timestamp = serializers.DateTimeField(format="%I:%M %p", required=False)
    timestamp = JsTimestampField(required=False)

    def create(self, validated_data):
        return Chats.objects.create(**validated_data)

    class Meta:
        model = Chats
        fields = ['roomId', 'chatId', 'user', 'timestamp', 'typ', 'text', 'seen', 'seen_by', 'delivered', 'delivered_to', 'media']
        read_only_fields = ['chatId', 'timestamp', 'user']

class RoomSerializer(serializers.ModelSerializer):
    # users = UserSerializer(many=True)
    user = serializers.SerializerMethodField()
    chats = serializers.SerializerMethodField()
    timestamp = JsTimestampField()
    unseenCount = serializers.SerializerMethodField()

    # def get_timestamp(self, obj):
    #     timetamp = timesince(obj.timestamp).split(',')[0] + " ago"
    #     # print(timetamp, "(((((((((((((())))))))))))))")
    #     return timetamp

    def get_unseenCount(self, obj):
        return obj.chats_set.filter(~Q(user=self.context['request'].user), seen=False).count()

    def get_chats(self, obj):
        return ChatSerializer(reversed(obj.chats_set.order_by('id').reverse()), many=True).data

    def get_user(self, obj):
        return UserSerializer(obj.users.filter(~Q(id=self.context['request'].user.id)).first()).data

    class Meta:
        model = Room
        fields = ['id', 'timestamp', 'unseenCount', 'user', 'chats',]