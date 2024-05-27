# Generated by Django 5.0.6 on 2024-05-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(
                fields=["deleted_at"], name="customer_deleted_3c8347_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="group",
            index=models.Index(
                fields=["deleted_at"], name="customer_gr_deleted_8b3d6b_idx"
            ),
        ),
    ]