# Generated by Django 5.0.2 on 2024-02-21 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Venues', '0004_remove_festivals_duration_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.PositiveIntegerField(blank=True, null=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Venues.places')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
    ]