# Generated by Django 3.2.13 on 2022-06-16 14:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=uuid.UUID, primary_key=True, serialize=False, unique=True),
        ),
    ]
