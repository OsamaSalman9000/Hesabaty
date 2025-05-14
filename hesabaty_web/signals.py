from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Invoice, Reservation


# ✅ 1. إنشاء UserProfile تلقائيًا
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, full_name=instance.username)


# ✅ 2. إنشاء Reservation تلقائيًا عند إنشاء فاتورة
@receiver(post_save, sender=Invoice)
def create_reservation_from_invoice(sender, instance, created, **kwargs):
    if created:
        Reservation.objects.create(
            apartment=instance.apartment,
            tenant=instance.tenant,
            invoice=instance,
            check_in_datetime=instance.check_in_datetime,
            check_out_datetime=instance.check_out_datetime,
            rent_type=instance.rent_type,
            is_active=True
        )