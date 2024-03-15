# Generated by Django 5.0.2 on 2024-03-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0011_alter_places_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='category',
            field=models.CharField(blank=True, choices=[('Adventure', 'Adventure'), ('Heritage', 'Heritage'), ('Pilgrimage', 'Pilgrimage'), ('Beach', 'Beach'), ('trending', 'trending')], default='', max_length=20, null=True),
        ),
    ]
