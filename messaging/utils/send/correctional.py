from typing import Literal


def correct_receptor(receptor: str) -> str | Literal[False]:
    """This is a function to convert other formats of iran phone number to standard."""
    if receptor.startswith("09") and len(receptor) == 11:
        return receptor
    elif receptor.startswith("+98") and len(receptor) == 13:
        return receptor.replace("+98", "0")
    elif receptor.startswith("9") and len(receptor) == 10:
        return receptor.replace("9", "09", 1)
    return False


def make_message_readable(
    message: str | list[str], customer_data: dict[str, str] | list[dict[str, str]]
) -> str | list[str]:
    """This is a function to change some variable text like %fullname to customer data."""
    if isinstance(message, list):
        if isinstance(customer_data, dict):
            messages = [
                i.replace("%name", customer_data.get("name", "")).replace(
                    "%fullname",
                    customer_data.get("fullname", ""),
                )
                for i in message
            ]
            return ",".join(messages)
        messages = [
            m.replace("%name", c.get("name", "")).replace(
                "%fullname",
                c.get("fullname", ""),
            )
            for m, c in zip(message, customer_data)
        ]
        return ",".join(messages)
    if isinstance(message, str):
        if isinstance(customer_data, list):
            messages = [
                message.replace("%name", c.get("name", "")).replace(
                    "%fullname",
                    c.get("fullname", ""),
                )
                for c in customer_data
            ]
            return messages
        return message.replace("%name", customer_data.get("name", "")).replace(
            "%fullname",
            customer_data.get("fullname", ""),
        )
