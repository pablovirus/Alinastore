# Generated by Django 3.2.13 on 2022-06-25 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20220625_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_currency',
        ),
    ]