# Generated by Django 5.0.4 on 2024-05-03 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0040_signupdata_old_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupdata',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='signupdata',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='signupdata',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='signupdata',
            name='phone',
            field=models.BigIntegerField(blank=True, default=123456789),
            preserve_default=False,
        ),
    ]
