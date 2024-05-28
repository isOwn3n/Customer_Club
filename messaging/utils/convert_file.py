"""This file is used to can import contacts from telegram to database."""

import orjson
from customers import models


def convert_data(file: bytes | str, with_name: bool = True):
    """Convert json data exported from telegram"""
    try:
        data = orjson.loads(file)
    except orjson.JSONDecodeError:
        raise FileNotFoundError("Invalid File")

    new_data = []
    data = data["contacts"]["list"]
    for i in data:
        if str(i["phone_number"]).startswith("0098"):
            i["phone_number"] = "0" + i["phone_number"][4:]

        if not str(i["phone_number"]).startswith("09"):
            continue

        if with_name:
            new_data.append([i["first_name"], i["last_name"], i["phone_number"]])
        else:
            new_data.append([i["phone_number"]])
    return new_data


def customers_from_telegram(file: bytes | str, include_name: bool = True):
    """This function used to create customers"""
    customers = convert_data(file, include_name)
    for customer in customers:
        if include_name:
            first_name, last_name, phone_number = customer
            models.Customer.objects.create_customer(  # type: ignore
                firstname=first_name, lastname=last_name, phone_number=phone_number
            )
        else:
            phone_number = customer[0]
            models.Customer.objects.create_customer(phone_number=phone_number)  # type: ignore
    return {"message": "Done"}
