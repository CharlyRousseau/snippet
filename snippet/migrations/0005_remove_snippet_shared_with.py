# Generated by Django 5.0.6 on 2024-07-24 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0004_snippet_shared_with'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='shared_with',
        ),
    ]
