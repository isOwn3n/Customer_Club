from django.db import models
from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
)


class Group(models.Model):
    group_english_name = models.CharField(max_length=100)
    group_persian_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "customer_groups"

    def __str__(self) -> str:
        return f"({self.group_english_name}) {self.group_persian_name}"


class CustomerManager(models.Manager):
    # def create
    def create_customer(
        self,
        firstname,
        lastname,
        member_of,
        points=0,
        birthday=None,
        wedding_date=None,
        phone_number=None,
    ):
        if not firstname:
            raise ValueError("Customers must have a firstname")

        if not lastname:
            raise ValueError("Customers must have a lastname")

        if not phone_number:
            raise ValueError("Customers must have a phone_number")

        customer = self.model(
            firstname=firstname,
            lastname=lastname,
            points=points,
            birthday=birthday,
            wedding_date=wedding_date,
            phone_number=phone_number,
        )
        customer.save()
        for group in member_of:
            try:
                customer.member_of.add(group)
            except:
                ...

        return customer


phone_regex = RegexValidator(
    regex=r"^(?:\+98|0)9\d{9}$", message="Invalid Phone Number"
)

phone_min_length = MinLengthValidator(
    11, "Phone number is too short, it must be 11 chars."
)
phone_max_length = MaxLengthValidator(
    11, "Phone number is too long, it must be 11 chars."
)


class Customer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            phone_regex,
            phone_min_length,
            phone_max_length,
        ],
    )
    member_of = models.ManyToManyField(Group)
    points = models.PositiveIntegerField(null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    wedding_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = CustomerManager()

    class Meta:
        db_table = "customer"

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname} ({self.phone_number})"
