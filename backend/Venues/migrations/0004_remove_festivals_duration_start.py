# Generated by Django 5.0.2 on 2024-02-21 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0003_remove_places_festivals_remove_places_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='festivals',
            name='duration_start',
        ),
    ]
