# Generated by Django 5.1.4 on 2025-01-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_ambience_cuisine_user_remove_restaurant_cuisine_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="sustainable",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="alcohol",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
