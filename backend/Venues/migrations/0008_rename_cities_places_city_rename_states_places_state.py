# Generated by Django 5.0.2 on 2024-03-12 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0007_uservisits'),
    ]

    operations = [
        migrations.RenameField(
            model_name='places',
            old_name='cities',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='places',
            old_name='states',
            new_name='state',
        ),
    ]