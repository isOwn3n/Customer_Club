from customers import models
from django.utils import timezone
from django.db.models.manager import BaseManager

from . import sending

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

def send_message_for_birthday(customers: BaseManager[models.Customer]):
    for i in customers:
        sending.send_birthday_and_wedding_day_message(True, i.pk)
