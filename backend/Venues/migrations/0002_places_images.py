# Generated by Django 5.0.2 on 2024-02-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='places/'),
        ),
    ]
