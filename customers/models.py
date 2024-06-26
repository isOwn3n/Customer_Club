from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
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

    def delete(self, *args, **kwargs):
        if self.pk == 1:
            raise ValidationError("Cannot delete this object.")
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        db_table = "customer_groups"
        # Add an index to speed up queries for non-deleted objects
        indexes = [
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self) -> str:
        return f"({self.group_english_name}) {self.group_persian_name}"


class CustomerManager(models.Manager):
    def create_customer(
        self,
        firstname=None,
        lastname=None,
        member_of=None,
        points=0,
        birthday=None,
        wedding_date=None,
        phone_number=None,
    ):
        if not phone_number:
            raise ValueError("Customers must have a phone_number")
        try:
            existing_customer = self.get(phone_number=phone_number)
            if existing_customer.deleted_at is not None:
                existing_customer.deleted_at = None
                existing_customer.firstname = firstname
                existing_customer.lastname = lastname
                existing_customer.birthday = birthday
                existing_customer.wedding_date = wedding_date
                existing_customer.points = points
                existing_customer.save()

                # All Customers Have to be in (All) Group
                initial_group = Group.objects.get(pk=1)
                existing_customer.member_of.add(initial_group)

                if member_of is not None:
                    for group in member_of:
                        try:
                            existing_customer.member_of.add(group)
                        except:
                            ...
                return existing_customer

            return existing_customer
        except self.model.DoesNotExist:
            customer = self.model(
                firstname=firstname,
                lastname=lastname,
                points=points,
                birthday=birthday,
                wedding_date=wedding_date,
                phone_number=phone_number,
            )
            customer.save()

            # All Customers Would be in (All) Group
            initial_group = Group.objects.get(pk=1)
            customer.member_of.add(initial_group)

            if member_of is not None:
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
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
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

    def delete(self, *args, **kwargs):
        self.member_of.clear()
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        initial_group = Group.objects.get(pk=1)
        self.member_of.add(initial_group)
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        db_table = "customer"
        # Add an index to speed up queries for non-deleted objects
        indexes = [
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname} ({self.phone_number})"
