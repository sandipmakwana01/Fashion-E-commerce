# Generated by Django 5.0.4 on 2024-04-21 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_signupdata_image_alter_signupdata_emailorphone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupdata',
            name='confirm_password',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]