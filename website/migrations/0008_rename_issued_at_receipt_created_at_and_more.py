# Generated by Django 5.1.5 on 2025-02-10 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receipt',
            old_name='issued_at',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='receipt',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='transaction',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.transaction'),
        ),
    ]
