from time import sleep
from celery import shared_task
from messaging.utils.send_message import general_sending_message


@shared_task
def send_message(message: str, customers_id: list[int]):
    sleep(10)
    return general_sending_message(message, customers_id).get("cost", 0)


@shared_task
def add(x, y):
    return x + y
