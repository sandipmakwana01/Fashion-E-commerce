# Generated by Django 5.0.4 on 2024-04-25 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_product_is_sale_product_sale_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='MenCategory',
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='MenProduct',
        ),
    ]
