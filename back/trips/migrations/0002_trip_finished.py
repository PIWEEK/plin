# Generated by Django 3.1 on 2020-12-15 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
