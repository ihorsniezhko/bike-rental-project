# Generated by Django 4.2.23 on 2025-06-19 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
