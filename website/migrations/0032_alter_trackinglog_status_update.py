# Generated by Django 5.1.5 on 2025-03-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackinglog',
            name='status_update',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], max_length=50),
        ),
    ]
