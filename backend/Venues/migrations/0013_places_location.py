# Generated by Django 5.0.2 on 2024-03-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0012_alter_places_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]