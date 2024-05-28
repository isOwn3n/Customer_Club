from .send import sending


def general_sending_message(message: str, customers_id: list[int]):
    if len(customers_id) > 1:
        if "%fullname" in message or "%name" in message or "%lastname" in message:
            return sending.send_array_of_messages(message, customers_id)
        return sending.send_one_message(message, customers_id)
    return sending.send_single_message(message, customers_id[0])
