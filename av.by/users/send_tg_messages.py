from telegram import Bot
import schedule
import threading
import time
import asyncio
from typing import List
from config import *
from .models import Message
from datetime import datetime
from django.utils import timezone
import uuid

# класс для отслеживания состояния работы планировщика
class Running():
    def __init__(self):
        self.is_running = True          # состояние работы планировщика
        self.count_sec = 0              # отсчёт секунд
        self.message = ""               # сообщение после изменения
        self.message_id = uuid.uuid4()  # уникальный id

    # проверка на предмет отмены отложенной отправки путём
    # удаления записи из базы
    def get_running(self, message) -> bool:
        # проверка раз 30 с
        if self.count_sec < 30:
            self.count_sec += 1
            return self.is_running
        else:
            try:
                # попытка прочитать запись
                obj = Message.objects.get(message_id=self.message_id)
                # забираем текст (на случай, если изменился)
                self.message = obj.text
                return self.is_running
            except:
                # если запись найти не удалось (отключаем планировщик)
                print("Отправка сообщения была отменена")
                return False


# отправка сообщения пользователю
async def sending(chat_id, message):
    bot = Bot(token=TELEGRAM_API_KEY)
    await bot.send_message(chat_id=chat_id, text=message)

def send_tg_msg(chat_ids: List, message: str, date_time: datetime = None) -> None:
    running = Running()
    def send_msg():
        text = message
        if running.message:
            text = running.message
        for chat_id in chat_ids:
            asyncio.run(sending(chat_id, text))
        try:
            # переводим изменяем статус отправки
            obj = Message.objects.get(message_id=running.message_id)
            obj.status = True
            obj.save()
        except:
            pass
        running.is_running = False
        return schedule.CancelJob

    # Добавляем задачу в планировщик
    if date_time:
        seconds = (date_time-datetime.now()).seconds
        schedule.every(seconds).seconds.do(send_msg)
        new_message = Message(text=message,
                              date_time=timezone.make_aware(date_time),
                              message_id=running.message_id,
                              status=False)
        new_message.save()
    else:
        schedule.every().seconds.do(send_msg)
        new_message = Message(text=message,
                              date_time=timezone.now(),
                              message_id=running.message_id,
                              status=False)
        new_message.save()



    # schedule.every(3).seconds.do(send_msg)

    # Функция для выполнения задач из планировщика
    def run_scheduler():
        while running.get_running(message=message):
            schedule.run_pending()
            time.sleep(1)

    # Запускаем выполнение задач в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()