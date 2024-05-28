from customers import models
from django.utils import timezone


def get_all_customers_they_birthday_is_today():
    customers = models.Customer.objects.filter(
        birthday=timezone.now(),
        deleted_at__is_null=None,
    )
    return customers


def get_all_customers_they_wedding_data_is_today():
    customers = models.Customer.objects.filter(
        wedding_date=timezone.now(),
        deleted_at__is_null=None,
    )
    return customers
