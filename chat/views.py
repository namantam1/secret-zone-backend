from django.shortcuts import render
from django.db.models import Q

from .models import Friends, User, Room
from .serializers import RoomSerializer, UserSerializer, ChatSerializer, UserLoginSerializer

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class UserLogin(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class NewRequest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        if User.objects.filter(~Q(id=request.user.id), username__iexact=username).exists():
            return Response({"exists":True}, status=200)
        return Response({'exists': False}, status=201)

    def post(self, request, username):
        data = request.data
        message = data.get("message")
        user = User.objects.filter(~Q(id=request.user.id), username__iexact=username).first()
        if user:
            print(user.friends.requests.all())
            user.friends.requests.add(request.user.id)
            request.user.friends.requested.add(user.id)
            return Response({"exists":True}, status=200)
        return Response({'exists': False}, status=201)

class RoomView(ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(users__in=[self.request.user])

class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.kwargs['pk'] = self.request.user.id
        return User.objects.all()

@api_view(['GET', 'POST'])
def save_chat(request):
    if request.method == "POST":
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
    return Response({})



