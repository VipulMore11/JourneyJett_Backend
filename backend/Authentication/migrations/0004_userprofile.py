# Generated by Django 5.0.2 on 2024-03-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_rename_users_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('User_profile', models.ImageField(blank=True, null=True, upload_to='Profilepic/')),
            ],
            options={
                'db_table': 'UserProfile',
            },
        ),
    ]
