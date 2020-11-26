# chat/urls.py
from django.urls import path
from . import views
from rest_framework.authtoken import views as rest_view
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', rest_view.obtain_auth_token),
    path('new-request/<username>/', views.NewRequest.as_view(), name="new_request"),
    path('user/', views.UserView.as_view(), name="user"),
    path('rooms/', views.RoomView.as_view(), name="room"),
    path('chat/', views.save_chat, name="chat"),
]