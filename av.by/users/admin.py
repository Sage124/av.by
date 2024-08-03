from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'photo', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'phone', 'photo', 'telegram_id', 'is_telegram_use')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_display = ('username', 'email', 'is_staff', 'id')
    search_fields = ('phone', 'username', 'email')
    ordering = ('phone',)

    actions = ['send_tg_message']

    @admin.action(description='Отправить сообщение в telegram')
    def send_tg_message(self, request, queryset: QuerySet):
        selected_items = queryset.values()
        # Создание нового массива объектов, содержащего только
        # ключи: "id", "username", "telegram_id" и "is_telegram_use"
        # этот подход позволяет также отправлять админов
        # (т.к. в составе их объекта есть time_delta
        users = [
            {
                "id": obj["id"],
                "username": obj["username"],
                "telegram_id": obj["telegram_id"],
                "is_telegram_use": obj["is_telegram_use"]
            } for obj in selected_items]
        request.session['users'] = list(users)
        return HttpResponseRedirect(reverse('send_tg_message'))

# вывод модели Message в админку
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'id', 'short_text', 'status')
    search_fields = ('date_time', 'text')
    readonly_fields = ('date_time', 'message_id', 'status')

    # часть текста сообщения
    def short_text(self, obj):
        return obj.text[:100]
    short_text.short_description = "Сокращённый текст"

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'short_text', 'user_create', 'status', 'id')
    search_fields = ('date_time', 'text', 'id')
    readonly_fields = ('date_time', 'user_create')

    # часть текста сообщения
    def short_text(self, obj):
        return obj.text[:100]

    short_text.short_description = "Сокращённый текст"

# онлайн-класс для удобного просмотра сообщений в чатах через админку
class ChatMessageInline(admin.TabularInline):  # Или используйте StackedInline
    model = Chat.messages.through
    extra = 0
    verbose_name = "Сообщение"
    verbose_name_plural = "Сообщения"

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id', 'messages__text')
    exclude = ('messages',)
    readonly_fields = ('users',)
    inlines = [ChatMessageInline]
