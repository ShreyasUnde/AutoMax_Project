# Generated by Django 4.0.5 on 2024-01-22 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_location_alter_profile_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone',
            new_name='phone_number',
        ),
    ]
