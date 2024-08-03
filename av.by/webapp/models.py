from django.db import models
from users.models import User

class Car(models.Model):
    # параметры
    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.CharField(max_length=200, verbose_name="Год")
    body_type = models.CharField(max_length=200, verbose_name="Кузов")
    transmission = models.CharField(max_length=200, verbose_name="Коробка передач")
    engine_type = models.CharField(max_length=200, verbose_name="Тип двигателя")
    drive_unit = models.CharField(max_length=200, verbose_name="Привод")
    engine_volume = models.CharField(max_length=200, verbose_name="Объём двигателя")
    vin = models.CharField(max_length=150, verbose_name="VIN", blank=True, default="")


    state = models.CharField(max_length=100, verbose_name="Состояние")
    mileage = models.IntegerField(verbose_name="Пробег, км")
    color = models.CharField(max_length=200, verbose_name="Цвет", default="Белый")
    interior_material = models.CharField(max_length=100, verbose_name="Материал салона", default="ткань")
    interior_color = models.CharField(max_length=100, verbose_name="Цвет салона", default="комби")


    abs = models.BooleanField(verbose_name="ABS", blank=True, default=False)
    esp = models.BooleanField(verbose_name="ESP", blank=True, default=False)
    anti_slip = models.BooleanField(verbose_name="Антипробуксовочная", blank=True, default=False)
    immobilizer = models.BooleanField(verbose_name="Иммобилайзер", blank=True, default=False)
    alarm_system = models.BooleanField(verbose_name="Сигнализация", blank=True, default=False)


    alloy_wheels = models.BooleanField(verbose_name="Легкосплавные диски", blank=True, default=False)
    roof_rails = models.BooleanField(verbose_name="Рейлинги на крыше", blank=True, default=False)
    trailer_coupling = models.BooleanField(verbose_name="Фаркоп", blank=True, default=False)


    seats = models.BooleanField(verbose_name="Сидений", blank=True, default=False)
    windshield = models.BooleanField(verbose_name="Лобового стекла", blank=True, default=False)
    mirrors = models.BooleanField(verbose_name="Зеркал", blank=True, default=False)
    steering_wheel = models.BooleanField(verbose_name="Руля", blank=True, default=False)
    autonomous_heater = models.BooleanField(verbose_name="Автономный отопитель", blank=True, default=False)

    engine_autorun = models.BooleanField(verbose_name="Автозапуск двигателя", blank=True, default=False)
    cruise_control = models.BooleanField(verbose_name="Круиз-контроль", blank=True, default=False)
    multimedia = models.BooleanField(verbose_name="Управление мультимедиа с руля", blank=True, default=False)
    electric_seat_adjustment = models.BooleanField(verbose_name="Электрорегулировка сидений", blank=True, default=False)
    front_electric_windows = models.BooleanField(verbose_name="Передние электро-стеклоподъёмники", blank=True, default=False)
    rear_electric_windows = models.BooleanField(verbose_name="Задние электро-стеклоподъёмники", blank=True, default=False)


    hatch = models.BooleanField(verbose_name="Люк", blank=True, default=False)
    panoramic_roof = models.BooleanField(verbose_name="Панорамная крыша", blank=True, default=False)


    front_cushions = models.BooleanField(verbose_name="Передние подушки", blank=True, default=False)
    side_cushions = models.BooleanField(verbose_name="Боковые подушки", blank=True, default=False)
    rear_cushions = models.BooleanField(verbose_name="Задние подушки", blank=True, default=False)


    xenon = models.BooleanField(verbose_name="Ксеноновые", blank=True, default=False)
    fog_lights = models.BooleanField(verbose_name="Противотуманные", blank=True, default=False)
    led_lights = models.BooleanField(verbose_name="Светодиодные", blank=True, default=False)


    aux_or_ipod = models.BooleanField(verbose_name="AUX или iPod", blank=True, default=False)
    bluetooth = models.BooleanField(verbose_name="Bluetooth", blank=True, default=False)
    cd_or_mp3 = models.BooleanField(verbose_name="CD или MP3", blank=True, default=False)
    usb = models.BooleanField(verbose_name="USB", blank=True, default=False)
    multimedia_screen = models.BooleanField(verbose_name="Мультимедийный экран", blank=True, default=False)
    regular_navigation = models.BooleanField(verbose_name="Штатная навигация", blank=True, default=False)


    rain_sensor = models.BooleanField(verbose_name="Датчик дождя", blank=True, default=False)
    rear_view_camera = models.BooleanField(verbose_name="Камера заднего вида", blank=True, default=False)
    parking_sensors = models.BooleanField(verbose_name="Парктроники", blank=True, default=False)
    monitoring_dead_zones_mirrors = models.BooleanField(verbose_name="Контроль мертвых зон на зеркалах", blank=True, default=False)

    climate_control = models.BooleanField(verbose_name="Климат-контроль", blank=True, default=False)
    conditioner = models.BooleanField(verbose_name="Кондиционер", blank=True, default=False)

    registration_country = models.CharField(max_length=100, verbose_name="Страна регистрации", blank=True, default="")
    accounting = models.CharField(max_length=100, verbose_name="Учёт", blank=True, default="")

    photo_1 = models.ImageField(null=True, blank=True, upload_to='Car', verbose_name="Фото 1")
    photo_2 = models.ImageField(null=True, blank=True, upload_to='Car', verbose_name="Фото 2")
    photo_3 = models.ImageField(null=True, blank=True, upload_to='Car', verbose_name="Фото 3")
    photo_4 = models.ImageField(null=True, blank=True, upload_to='Car', verbose_name="Фото 4")
    photo_5 = models.ImageField(null=True, blank=True, upload_to='Car', verbose_name="Фото 5")
    youtube = models.URLField(verbose_name="Видео из YouTube", blank=True, default="")

    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена")

    city = models.CharField(max_length=200, verbose_name="Город")

    name = models.CharField(max_length=200, verbose_name="Имя продавца", blank=True, default="")
    phone_1 = models.CharField(max_length=9, verbose_name="Номер телефона 1", default="", blank=True)
    phone_2 = models.CharField(max_length=9, verbose_name="Номер телефона 2", default="", blank=True)
    phone_3 = models.CharField(max_length=9, verbose_name="Номер телефона 3", default="", blank=True)

    user_create = models.ForeignKey(User, verbose_name="Пользователь, создавший запись", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{str(self.brand)} {str(self.model)} {str(self.year)}"

    class Meta:
        verbose_name = "Легковой автомобиль"
        verbose_name_plural = "Легковые авто"
