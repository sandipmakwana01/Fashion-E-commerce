# Generated by Django 5.0.4 on 2024-04-20 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='signupdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailorphone', models.TextField()),
                ('username', models.TextField()),
                ('password', models.TextField()),
            ],
        ),
    ]