from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from customers.models import Group


class BuiltInMessage(models.Model):
    message = models.CharField(max_length=900)
    is_birthday = models.BooleanField(default=False)
    is_wedding_date = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        db_table = "messages"
        # Add an index to speed up queries for non-deleted objects
        indexes = [
            models.Index(fields=["deleted_at"]),
        ]


# This Model used for create chart of sent messages
class SendLog(models.Model):
    count = models.PositiveIntegerField()
    gruops = models.ManyToManyField(Group)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at.year}-{self.created_at.month}-{self.created_at.day} ({self.count})"

    class Meta:
        db_table = "chart_data"


ACTION_CHOICES = (
    ("CREATE_CUSTOMER", "created a new customer"),
    ("CREATE_USER", "created a new user"),
    ("CREATE_GROUP", "created a new group for customers"),
    ("CREATE_MESSAGE", "created a new message for birthday or wedding day"),
    ("DELETE_CUSTOMER", "deleted a customer"),
    ("DELETE_USER", "deleted a user"),
    ("DELETE_GROUP", "deleted a group"),
    ("DELETE_MESSAGE", "deleted one of the built in messages"),
    ("UPDATE_CUSTOMER", "updated one of the customers"),
    ("UPDATE_USER", "updated one of the users"),
    ("UPDATE_GROUP", "updated one of the groups"),
    ("UPDATE_MESSAGE", "updated one of the messages"),
)


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} ({self.user.username})"

    def save(self, *args, **kwargs):
        # Prevent updating existing instances
        if self.pk:
            raise ValueError("Updating existing instances is not allowed")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Deleting instances is not allowed")

    class Meta:
        db_table = "actions"


REASON_CHOICES = (
    ("BIRTHDAY", "Sent a message for birthday."),
    ("WEDDING_DATE", "Sent a message for wedding date."),
    ("GROUP_SINGLE_MESSAGE", "Sent a single message for a group/groups."),
    (
        "GROUP_ARRAY_MESSAGE",
        "Sent an special message for each customer in group/groups (Array message).",
    ),
    ("SEND_A_MESSAGE", "Sent a message to a customer."),
    ("REMAIN_CREDIT_MESSAGE", "Sent a warning message to a admin to recharge credit."),
    ("WARNING_MESSAGE", "Sent a warning message to a admin to for a problem."),
    ("SEND_A_MESSAGE_TO_A_NOT_CUSTOMER", "Sent a message to not in db contact."),
)


class MessageLog(models.Model):
    message_id = models.PositiveIntegerField()
    status = models.IntegerField()
    status_text = models.CharField(max_length=500)
    message = models.TextField()
    cost = models.IntegerField()
    receptor = models.CharField(max_length=11)
    reason = models.CharField(max_length=255, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.status}, {self.message_id}): {self.message}"

    class Meta:
        db_table = "message_log"
