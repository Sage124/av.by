from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .serializers import *
from .send_tg_messages import *
from .models import *
from django.contrib import messages
from django.db.models import Count

####### АВТОРИЗАЦИЯ #######

# register
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# retrieve
class UserRetrieveView(TokenVerifyView):
    serializer_class = UserRetrieveSerializer

# update (for telegram info)
class UpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

# login
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# verify
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

# refresh
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

# logout
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = tokens.RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400)

# ####### КАСТОМИЗАЦИЯ JWT-ТОКЕНОВ #######
# class MyTokenObtainPairView(views.TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# отправка сообщения в telegram
def send_tg_message(request):
    selected_items = request.session.get('users')
    if request.method == 'POST':
        date = request.POST.get('date')
        # formated_data = date.replace("T", " ")
        datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M") if date else None

        text = request.POST.get('text')

        # получаем telegram_id выбранных пользаков
        telegram_ids = [item['telegram_id'] for item in selected_items]
        # срезаем тех, кто не привязал телегу (без telegram_id)
        filtered_tg_ids = list(filter(None, telegram_ids))

        # передаём в планировщик
        send_tg_msg(filtered_tg_ids, text, datetime_object)

        # Очищаем сессию
        request.session['selected_items'] = None
        # Добавляем уведомление об успехе на страницу админки
        messages.success(request, f'Сообщение добавлено в очередь отправки')
        # Возвращаемся на страницу админки с пользователями
        return HttpResponseRedirect(reverse('admin:users_user_changelist'))
    return render(request, 'admin/send_message.html')

# ################## Чат ######################
# создать сообщение в чате или новый чат с сообщением (если чата ещё нет)
class ChatMessageCreateView(generics.CreateAPIView):
    # queryset = ChatMessage.objects.all()
    # serializer_class = ChatMessageCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        message_text = request.data.get('text')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        chat = Chat.objects.filter(users__in=[self.request.user, user]).annotate(num_users=Count('users')).filter(
            num_users=2).first()

        if not chat:
            chat = Chat.objects.create()
            chat.users.add(self.request.user, user)

        chat_message = ChatMessage.objects.create(
            text=message_text,
            user_create=self.request.user,
        )

        chat.messages.add(chat_message)

        serializer = ChatMessageCreateSerializer(chat_message)
        return Response({"info": "Сообщение создано",
                         "message": serializer.data,
                         "chat_id": chat.id,
                         "users": [
                             {
                                 "id": f"{user.id}",
                                 "username": f"{user.username}",
                                 "photo": f"{request.build_absolute_uri(user.photo.url) if user.photo else None}"
                             },
                             {
                                 "id": f"{self.request.user.id}",
                                 "username": f"{self.request.user.username}",
                                 "photo": f"{request.build_absolute_uri(self.request.user.photo.url) if self.request.user.photo else None}"
                             }
                         ]
                         }, status=status.HTTP_201_CREATED)

        # chat, created = Chat.objects.get_or_create()
        # chat.users.add(self.request.user)
        # chat.users.add(user)
        #
        # chat_message = ChatMessage.objects.create(
        #     text=message_text,
        #     user_create=request.user,
        #     chat=chat
        # )
        #
        # chat.messages.add(chat_message)
        #
        # serializer = ChatMessageSerializer(chat_message)
        # return Response({"message": "Сообщение создано", "data": serializer.data}, status=status.HTTP_201_CREATED)

# получить список всех чатов текущего пользователя
class ChatMessageRetrieveView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(users=user)

# обновить сообщение в чате
class ChatMessageUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ChatMessageUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = ChatMessage.objects.all()
