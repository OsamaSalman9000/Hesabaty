# Generated by Django 5.2 on 2025-05-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabaty_web', '0003_tenant_created_at_tenant_user_expense_rental'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_recurring',
            field=models.BooleanField(default=False, verbose_name='شهري متكرر'),
        ),
    ]
