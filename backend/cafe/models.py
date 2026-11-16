
from django.db import models
from django.conf import settings


# 1. Компьютерийн төрөл - Лавлах
class ComputerType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 2. Компьютер - Лавлах
class Computer(models.Model):
    STATUS_CHOICES = [
        ('available', 'Сул'),
        ('occupied', 'Завгүй'),
        ('maintenance', 'Засвартай'),
    ]

    name = models.CharField(max_length=100, unique=True)
    computer_type = models.ForeignKey(
        ComputerType,
        on_delete=models.PROTECT,
        related_name='computers'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    specifications = models.TextField(blank=True)

    def __str__(self):
        return self.name


# 3. Үнийн тариф - Лавлах
class Pricing(models.Model):
    computer_type = models.ForeignKey(
        ComputerType,
        on_delete=models.PROTECT
    )
    name = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name


# 4. Нэмэлт үйлчилгээ - Лавлах
class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# 5. Хэрэглэгч - Бүртгэл
class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# 6. Компьютерийн захиалга - Бүртгэл
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Хүлээгдэж буй'),
        ('confirmed', 'Баталгаажсан'),
        ('completed', 'Дууссан'),
        ('cancelled', 'Цуцлагдсан'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )
    computer = models.ForeignKey(
        Computer,
        on_delete=models.PROTECT
    )
    pricing = models.ForeignKey(
        Pricing,
        on_delete=models.PROTECT
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.computer}"


# 7. Төлбөр - Бүртгэл
class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Бэлэн мөнгө'),
        ('card', 'Карт'),
        ('qpay', 'QPay'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Хүлээгдэж буй'),
        ('paid', 'Төлөгдсөн'),
        ('failed', 'Амжилтгүй'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Payment #{self.id}"
