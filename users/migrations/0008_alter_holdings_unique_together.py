# Generated by Django 4.0.4 on 2022-05-07 19:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_remove_holdings_id_holdings_auto_increment_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='holdings',
            unique_together={('symbol_name', 'user')},
        ),
    ]
