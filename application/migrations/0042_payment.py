# Generated by Django 5.0.4 on 2024-05-03 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0041_signupdata_address_signupdata_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.TextField()),
            ],
        ),
    ]
