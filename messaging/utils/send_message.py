from typing import List
from .send import sending
from customers import models


def general_sending_message(message: str, customers_id: list[int]):
    if len(customers_id) > 1:
        if "%fullname" in message or "%name" in message or "%lastname" in message:
            return sending.send_array_of_messages(message, customers_id)
        return sending.send_one_message(message, customers_id)
    return sending.send_single_message(message, customers_id[0])


def get_all_customers_in_a_group(groups_id: List[int]):
    customers_id = []
    for group_id in groups_id:
        customers_id += models.Customer.objects.filter(
            member_of__id=group_id
        ).values_list("id", flat=True)
    return customers_id
