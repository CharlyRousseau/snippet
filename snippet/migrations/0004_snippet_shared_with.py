# Generated by Django 5.0.6 on 2024-07-24 08:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0003_alter_snippet_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_snippets', to=settings.AUTH_USER_MODEL),
        ),
    ]
