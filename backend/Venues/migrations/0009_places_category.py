# Generated by Django 5.0 on 2024-03-13 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0008_rename_cities_places_city_rename_states_places_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='category',
            field=models.CharField(blank=True, choices=[('Adventure', 'None'), ('Heritage', 'Yes'), ('Pilgrimige', 'No'), ('Beach', 'Beach')], default='', max_length=20, null=True),
        ),
    ]
