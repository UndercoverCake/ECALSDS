# Generated by Django 5.1.5 on 2025-02-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_rename_created_at_receipt_issued_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
