# Generated by Django 5.0.2 on 2024-03-09 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0002_rename_user_users'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authtoken', '0003_tokenproxy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]
