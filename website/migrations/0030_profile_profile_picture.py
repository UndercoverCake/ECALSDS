# Generated by Django 5.1.5 on 2025-02-27 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0029_order_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
