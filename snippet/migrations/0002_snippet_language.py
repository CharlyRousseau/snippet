# Generated by Django 5.0.6 on 2024-06-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("snippet", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="snippet",
            name="language",
            field=models.CharField(default="plaintext", max_length=100),
        ),
    ]
