from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .views import *
from django.urls import path

urlpatterns = [
    path('v1/user/register/', RegisterView.as_view(), name='user_register'),
    path('v1/user/retrieve/', UserRetrieveView.as_view(), name='user_retrieve'),
    path('v1/user/update/<int:pk>', UpdateView.as_view(), name='user_update'),

    path('v1/user/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/user/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('v1/user/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('v1/user/logout/', LogoutView.as_view(), name='logout'),
    path('v1/user/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('send_tg_message/', send_tg_message, name='send_tg_message'),

    path('v1/chat_message/create/', ChatMessageCreateView.as_view(), name='chat_message_create'),
    path('v1/chat_message/list/', ChatMessageRetrieveView.as_view(), name='chat_message_list_view'),
    path('v1/chat_message/update/<int:pk>', ChatMessageUpdateView.as_view(), name='chat_message_update_view'),
]
