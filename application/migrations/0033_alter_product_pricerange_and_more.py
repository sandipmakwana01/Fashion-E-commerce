# Generated by Django 5.0.4 on 2024-04-27 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0032_alter_product_pricerange_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pricerange',
            field=models.ForeignKey(default='100', on_delete=django.db.models.deletion.CASCADE, to='application.pricerange'),
        ),
        migrations.AlterField(
            model_name='trendyproduct',
            name='pricerange',
            field=models.ForeignKey(default='100', on_delete=django.db.models.deletion.CASCADE, to='application.pricerange'),
        ),
    ]
