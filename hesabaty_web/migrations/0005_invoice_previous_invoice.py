# Generated by Django 5.2 on 2025-05-15 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabaty_web', '0004_expense_is_recurring'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='previous_invoice',
            field=models.ForeignKey(blank=True, help_text='إذا كانت هذه الفاتورة دفع جزئي لفاتورة سابقة', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partial_payments', to='hesabaty_web.invoice'),
        ),
    ]
