# Generated by Django 3.2.13 on 2022-06-30 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_order_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone_no',
            new_name='telephone',
        ),
    ]
