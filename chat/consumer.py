# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import UserSerializer, ChatSerializer
from .models import Profile, Room, Chats

token_athentication = TokenAuthentication()

class ChatConsumer(WebsocketConsumer):
    @property
    def get_token(self):
        try:
            return dict((self.scope['query_string'].decode().split("="),))
        except Exception as e:
            print(e)
            return dict(error=e)

    # def _is_authenticated(self):
    #     # self.user_id = self.scope['url_route']['kwargs']['user_id']
    #     # print(self.get_token())
    #     if self.scope['user'].is_authenticated:
    #         self.user = self.scope['user']
    #         return True
    #     # try:
    #     # print(self.get_token)
    #     user, _ = token_athentication.authenticate_credentials(self.get_token['token'])
    #     print(user, _)
    #     self.scope['user'] = user
    #     return True

    def _is_authenticated(self):
        if self.scope['user'].is_authenticated:
            self.user = self.scope['user']
            return True

        try:
            self.validate_token = JWTAuthentication().get_validated_token(raw_token=self.get_token.get('token'))
        except InvalidToken as e:
            print(e)
            return False
            
        self.user = JWTAuthentication().get_user(validated_token=self.validate_token)
        # if str(self.user.id) == str(self.user_id):
        self.scope['user'] = self.user
        return True
        # return False


    def get_room_group_name(self, id):
        return "room_%s" % id

    def connect(self):
        if self._is_authenticated():
            self.user = self.scope['user']
            self.room_ids = [room.id for room in self.user.room_set.all()]
            # self.room_name = self.scope['url_route']['kwargs']['room_name']
            # self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            print(self.room_ids)
            for room in self.room_ids:
                async_to_sync(self.channel_layer.group_add)(
                    self.get_room_group_name(room),
                    self.channel_name
                )

            self.accept()
            self.update_status(online=True)
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_ids'):
            print(self.room_ids)
            for room in self.room_ids:
                async_to_sync(self.channel_layer.group_discard)(
                    self.get_room_group_name(room),
                    self.channel_name
                )
            self.update_status(online=False)

    def update_status(self, online=False):
        profile = Profile.objects.get(user=self.user)
        if online:
            profile.online = True
        else:
            profile.online = False
            profile.last_seen = datetime.now()
        profile.save()
        user = UserSerializer(instance=self.user).data
        user['online'] = online
        user['lastSeen'] = timezone.now().timestamp() * 1000
        print(user)
        for room in self.room_ids:
            async_to_sync(self.channel_layer.group_send)(
                self.get_room_group_name(room),
                {
                    "type": "status_upadate_send",
                    "message": {
                        'type': "online_status",
                        'roomId': room,
                        "user": user
                    }
                }
            )
            print(room, online, "** status send **")

    def update_seen_status(self, message):
        room_id = message.get('roomId')
        room = Room.objects.filter(users__in=[self.user], id=room_id).first()
        if room:
            k = room.chats_set.filter(~Q(user=self.user),seen=False).update(seen=True)
            # print(k)
            if k:
            # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.get_room_group_name(room_id),
                    {
                        "type": "send_status_seen",
                        "message": {
                            "type": "update_message_status",
                            'roomId': room_id
                        }
                    }
                ) 


    def message_receive(self, message):
        serializer = ChatSerializer(data=message)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.user)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.get_room_group_name(serializer.data['roomId']),
                {
                    "type": "chat_message",
                    "message":serializer.data
                }
            )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['text']
        print(text_data)
        if(text_data_json.get('type') == 'message'):
            self.message_receive(text_data_json.get('data'))
        elif(text_data_json.get('type') == 'update_message_status'):
            self.update_seen_status(text_data_json)
        

    # Receive message from room group
    def chat_message(self, event):
        # print(event)
        message = event['message']
        data = {
            'type': 'message',
            'message': message
        }
        print(data, "## messafe ##")

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))

    def status_upadate_send(self, event):
        message = event['message']
        print(message, "## status update ##")
        self.send(text_data=json.dumps(message))

    def send_status_seen(self, event):
        message = event['message']
        data = {
            'type': 'seenStatus',
            'message': message
        }
        print(data, "#$# status seen update #$#")
        self.send(text_data=json.dumps(data))