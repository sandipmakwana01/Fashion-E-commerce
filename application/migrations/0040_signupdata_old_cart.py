# Generated by Django 5.0.4 on 2024-05-01 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0039_delete_trendyproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupdata',
            name='old_cart',
            field=models.TextField(blank=True),
        ),
    ]
