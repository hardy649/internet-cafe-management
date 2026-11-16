from django.contrib import admin
from .models import (
    ComputerType,
    Computer,
    Pricing,
    Service,
    Customer,
    Booking,
    Payment,
)


@admin.register(ComputerType)
class ComputerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'computer_type', 'status')
    list_filter = ('computer_type', 'status')
    search_fields = ('name',)


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'computer_type', 'price_per_hour')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'category')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'computer',
        'start_time', 'end_time',
        'total_price', 'status'
    )
    list_filter = ('status',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'method', 'status')
    list_filter = ('method', 'status')
