from django.db.models.signals import post_migrate
from django.dispatch import receiver
from customers.models import Group


@receiver(post_migrate)
def add_group(sender, **kwargs):
    if not Group.objects.filter(group_english_name="All").exists():
        Group.objects.create(group_english_name="All", group_persian_name="همه")
