# Generated by Django 2.2.5 on 2023-06-07 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LinkedInScraper', '0004_favoriteduser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='linkedin_id',
            new_name='profile_id',
        ),
    ]
