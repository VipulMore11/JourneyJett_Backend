# Generated by Django 5.0.2 on 2024-02-21 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0002_places_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='places',
            name='festivals',
        ),
        migrations.RemoveField(
            model_name='places',
            name='images',
        ),
        migrations.AddField(
            model_name='festivals',
            name='festivals',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festivals', to='Venues.places'),
        ),
        migrations.CreateModel(
            name='PlacesImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('places_image', models.ImageField(blank=True, null=True, upload_to='places/')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Venues.places')),
            ],
            options={
                'db_table': 'places_images',
            },
        ),
    ]