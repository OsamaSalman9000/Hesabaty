from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Building
from .models import Tenant
from django import forms
from .models import Apartment, Invoice, Tenant
from django.utils import timezone
from .models import Expense
from django.db.models import F
from .models import Apartment, Invoice
from django import forms
from .models import Invoice

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="اسم المستخدم", widget=forms.TextInput())
    password = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput())

class BuildingWithApartmentsForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'apartment_count']

    # توزيع الشقق
    apartment_distribution = forms.CharField(
        label='توزيع الشقق',
        help_text='اكتب توزيع الشقق بهذا الشكل: 10-2-yes,5-1-no (يعني 10 شقق غرفتين وصالة، 5 شقق غرفة بدون صالة)'
    )

class ApartmentForm(forms.Form):
    number = forms.IntegerField(label="رقم الشقة", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    room_count = forms.IntegerField(label="عدد الغرف", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    has_living_room = forms.BooleanField(label="هل فيها صالة؟", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستأجر'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الجوال'}),
        }

class InvoiceForm(forms.Form):
    tenant_name = forms.CharField(label="اسم المستأجر", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tenant_phone = forms.CharField(label="رقم الجوال", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(),
        label="الشقة",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    amount = forms.DecimalField(label="المبلغ الكلي", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    amount_paid = forms.DecimalField(
        label="المبلغ المدفوع (اختياري)",
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    rent_type = forms.ChoiceField(
        choices=Invoice.RENT_TYPE_CHOICES,
        label="نوع الإيجار",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    check_in_datetime = forms.DateTimeField(label="تاريخ الدخول", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    check_out_datetime = forms.DateTimeField(label="تاريخ الخروج", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'custom_category', 'description', 'project_scope', 'is_recurring']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class PaymentForm(forms.Form):
    invoice = forms.ModelChoiceField(
        queryset=Invoice.objects.all(),
        label="اختر الفاتورة",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amount = forms.DecimalField(
        label="المبلغ المدفوع",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )