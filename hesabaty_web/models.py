from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# 🟦 1. UserProfile (امتداد لـ Django User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    PRIVILEGE_CHOICES = [
        ('admin', 'مدير'),
        ('assistant_manager', 'نائب مدير'),
        ('employee', 'موظف استقبال'),
    ]
    privileges = models.CharField(max_length=20, choices=PRIVILEGE_CHOICES, default='employee')

    def __str__(self):
        return self.full_name


# 🟦 2. Buildings Table
class Building(models.Model):
    name = models.CharField(max_length=100)
    apartment_count = models.IntegerField()
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# 🟦 3. Apartments Table
class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    room_count = models.IntegerField()
    has_living_room = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.building.name})"


# 🟦 4. Tenants Table
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


# 🟦 5. Invoices Table
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ تعريف ثابت خيارات نوع الإيجار
    RENT_TYPE_CHOICES = [
        ('daily', 'يومي'),
        ('monthly', 'شهري'),
        ('yearly', 'سنوي'),
    ]
    rent_type = models.CharField(max_length=20, choices=RENT_TYPE_CHOICES)

    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"فاتورة {self.id} - {self.tenant.name}"

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def is_fully_paid(self):
        return self.total_paid >= self.amount

# 🟦 6. Reservations Table
class Reservation(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField()
    rent_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"حجز {self.tenant.name} - {self.apartment.name}"


# 7. Expense Table
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'إيجار'),
        ('electricity', 'كهرباء'),
        ('water', 'ماء'),
        ('salary', 'راتب'),
        ('other', 'أخرى'),
    ]

    PROJECT_SCOPE_CHOICES = [
        ('related', 'مرتبط بالمشروع'),
        ('unrelated', 'غير مرتبط بالمشروع'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    custom_category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False, verbose_name="شهري متكرر")
    project_scope = models.CharField(
        max_length=10,
        choices=PROJECT_SCOPE_CHOICES,
        default='related',
        verbose_name="نطاق المصروف"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ريال - {self.get_category_display()}"

# 8. Rental Table
class Rental(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rentals')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE, related_name='rental')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.name} استأجر {self.apartment.name}"

# 9. Payment Table
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"دفعة {self.amount} لفاتورة {self.invoice.id}"