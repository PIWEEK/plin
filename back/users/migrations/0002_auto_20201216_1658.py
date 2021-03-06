# Generated by Django 3.1 on 2020-12-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, max_length=150, null=True, unique=True, verbose_name='username'),
        ),
    ]
