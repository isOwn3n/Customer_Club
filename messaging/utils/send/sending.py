from typing import Literal
from .correctional import make_message_readable

from django.conf import settings
from rest_framework.exceptions import APIException
from customers import models
from messaging import models as m_models
import kavenegar

API_KEY = settings.KAVENEGAR_API_KEY
SMS_SENDER = settings.KAVENEGAR_SMS_SENDER


def send_message(
    message: str, receptor: str, message_reason: str | None
) -> dict[str, int]:
    total_cost = 0
    try:
        api = kavenegar.KavenegarAPI(API_KEY)
        params = {"sender": SMS_SENDER, "receptor": receptor, "message": message}
        response = api.sms_send(params)
        if message_reason:
            for i in response:
                m_models.MessageLog.objects.create(
                    message_id=i.get("messageid"),
                    status=i.get("status"),
                    status_text=i.get("statustext"),
                    message=i.get("message"),
                    cost=i.get("cost"),
                    receptor=i.get("receptor"),
                    reason=message_reason,
                )
        cost = [i["cost"] for i in response]
        total_cost += sum(cost)
        return {"cost": total_cost}
    except kavenegar.APIException as e:
        e = str(e)  # type: ignore
        if "418" in e:
            raise kavenegar.APIException(
                {"message": "No credit Available", "status": 418}
            )
        elif "413" in e:
            raise kavenegar.APIException(
                {"message": "Too long message!", "status": 413}
            )
        elif "411" in e:
            raise kavenegar.APIException(
                {"message": "Invalid Receptor!", "status": 411}
            )
        elif "414" in e:
            raise kavenegar.APIException(
                {"message": "Too many receptors.", "status": 414}
            )
        else:
            raise kavenegar.APIException(str(e))
    except kavenegar.HTTPException:
        raise kavenegar.HTTPException("No Connection!")


def send_array(
    messages: list[str],
    receptors: list[str],
    senders: list[str],
    message_reason: str | None,
) -> dict[str, int]:
    try:
        total_cost = 0
        api = kavenegar.KavenegarAPI(API_KEY)
        for _ in range(0, len(receptors), 200):
            params = {
                "sender": f"{senders[0:199]}",
                "receptor": f"{receptors[0:199]}",
                "message": f"{messages[0:199]}",
            }
            del senders[0:199]
            del receptors[0:199]
            del messages[0:199]

            response = api.sms_sendarray(params)
            if message_reason:
                for i in response:
                    m_models.MessageLog.objects.create(
                        message_id=i.get("messageid"),
                        status=i.get("status"),
                        status_text=i.get("statustext"),
                        message=i.get("message"),
                        cost=i.get("cost"),
                        receptor=i.get("receptor"),
                        reason=message_reason,
                    )

            cost = [i["cost"] for i in response]
            total_cost += sum(cost)
        return {"cost": total_cost}
    except kavenegar.APIException as e:
        e = e.decode()  # type: ignore
        if "418" in e:
            raise kavenegar.APIException(
                {"message": "No credit Available", "status": 418}
            )
        elif "413" in e:
            raise kavenegar.APIException(
                {"message": "Too long message!", "status": 413}
            )
        elif "411" in e:
            raise kavenegar.APIException(
                {"message": "Invalid Receptor!", "status": 411}
            )
        elif "414" in e:
            raise kavenegar.APIException(
                {"message": "Too many receptors.", "status": 414}
            )
        else:
            raise kavenegar.APIException(str(e))
    except kavenegar.HTTPException:
        raise kavenegar.HTTPException("No Connection!")


def send_single_message(message: str, pk: int) -> dict[str, int]:
    """This is a function to send message to a single customer."""
    try:
        customer = models.Customer.objects.get(deleted_at__isnull=True, pk=pk)
    except models.Customer.DoesNotExist:
        raise models.Customer.DoesNotExist("Customer Does Not Exist.")

    firstname = customer.firstname if customer.firstname is not None else ""
    lastname = customer.lastname if customer.lastname is not None else ""
    changed_message = make_message_readable(
        message,
        {
            "name": firstname,
            "lastname": lastname,
            "fullname": f"{firstname} {lastname}",
        },
    )

    if isinstance(changed_message, str):
        message = changed_message
    return send_message(message, customer.phone_number, "SEND_A_MESSAGE")


def send_single_message_to_not_customer(message: str, receptor: str):
    return send_message(message, receptor, "SEND_A_MESSAGE_TO_A_NOT_CUSTOMER")


def send_array_of_messages(message: str, customers_id: list[int]) -> dict[str, int]:
    """this is a function to send a lot of diffrent messages."""
    if not "%name" in message and not "%fullname" in message:
        return send_one_message(message, customers_id)
    customers = models.Customer.objects.filter(id__in=customers_id)
    if customers:
        receptors = [i.phone_number for i in customers]
        customers_data = [
            {
                "name": c.firstname,
                "lastname": c.lastname,
                "fullname": f"{c.firstname} {c.lastname}",
            }
            for c in customers
        ]
        messages = make_message_readable(message, customers_data)
        senders = SMS_SENDER * len(receptors)
        if isinstance(messages, list):
            return send_array(messages, receptors, senders, "GROUP_ARRAY_MESSAGE")

    raise ValueError("No Customer Available")


def send_one_message(message: str, customers_id: list[int]) -> dict[str, int]:
    """This function send one message to some receptor"""
    total_cost = 0
    customers = models.Customer.objects.filter(id__in=customers_id)
    if customers:
        receptors = [i.phone_number for i in customers]

        for _ in range(0, len(receptors), 200):
            total_cost += send_message(
                message, ",".join(receptors[0:199]), "GROUP_SINGLE_MESSAGE"
            )["cost"]
        return {"cost": total_cost}
    raise ValueError("No Customer Available")


def send_birthday_and_wedding_day_message(
    is_birthday: bool, customer_id: list[int]
) -> dict[str, int] | None:
    try:
        message = m_models.BuiltInMessage.objects.get(
            is_birthday=is_birthday,
            is_wedding_date=not is_birthday,
        )
    except m_models.BuiltInMessage.DoesNotExist:
        return

    try:
        customer = models.Customer.objects.get(pk=customer_id)
    except m_models.BuiltInMessage.DoesNotExist:
        return

    try:
        if is_birthday:
            return send_message(message.message, customer.phone_number, "BIRTHDAY")
        return send_message(message.message, customer.phone_number, "WEDDING_DATE")
    except:
        send_warning_message("پیام برای کاربر ارسال نشد.")
        return


def send_remain_credit_warning():
    """This is a function to send warning message to admin to charge kavenegar account."""
    admin_phone_number = settings.ADMIN_PHONE_NUMBER
    send_message("حساب خود را شارژ کنيد", admin_phone_number, "REMAIN_CREDIT_MESSAGE")


def send_warning_message(message: str):
    """This is a function to send warning message to admin."""
    admin_phone_number = settings.ADMIN_PHONE_NUMBER
    try:
        send_message(message, admin_phone_number, "WARNING_MESSAGE")
    except:
        ...


def check_sending_message_is_possible(
    message: str, customer_count: int
) -> tuple[Literal[True], int] | Literal[False]:
    if len(message) == 0 or customer_count == 0:
        return False
    message = (
        message.replace("%name", "آقای")
        .replace("%fullname", "آقای فلانی")
        .replace("%lastname", "فلانی")
    )
    response = send_message(message, "09123456789", None)
    credit = get_kavenegar_info()
    if response["cost"] * customer_count > credit - 10000:
        return False
    return (True, response["cost"])


def get_kavenegar_info() -> int:
    api = kavenegar.KavenegarAPI(API_KEY)
    try:
        response = api.account_info()
        return response["remaincredit"]
    except kavenegar.APIException as e:
        raise e
    except kavenegar.HTTPException as e:
        raise e
