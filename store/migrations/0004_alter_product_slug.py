# Generated by Django 3.2.13 on 2022-06-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=None, primary_key=True, serialize=False, unique=True),
        ),
    ]
