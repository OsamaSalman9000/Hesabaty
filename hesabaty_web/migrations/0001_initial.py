# Generated by Django 5.2 on 2025-05-04 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('apartment_count', models.IntegerField()),
                ('is_canceled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('room_count', models.IntegerField()),
                ('has_living_room', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.building')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rent_type', models.CharField(choices=[('daily', 'يومي'), ('monthly', 'شهري'), ('yearly', 'سنوي')], max_length=20)),
                ('check_in_datetime', models.DateTimeField()),
                ('check_out_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.apartment')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.building')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_datetime', models.DateTimeField()),
                ('check_out_datetime', models.DateTimeField()),
                ('rent_type', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.apartment')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.invoice')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabaty_web.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('privileges', models.CharField(choices=[('admin', 'مدير'), ('assistant_manager', 'نائب مدير'), ('employee', 'موظف استقبال')], default='employee', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
