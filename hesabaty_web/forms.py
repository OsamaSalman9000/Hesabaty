from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Building
from .models import Tenant
from django import forms
from .models import Apartment, Invoice, Tenant
from django.utils import timezone
from django import forms
from .models import Expense

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
    tenant_phone = forms.CharField(label="رقم جوال المستأجر", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(),
        label="الشقة",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    amount = forms.DecimalField(label="المبلغ", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_paid = forms.DecimalField(label="المبلغ المدفوع", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    rent_type = forms.ChoiceField(
        choices=Invoice.RENT_TYPE_CHOICES,
        label="نوع الإيجار",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    check_in_datetime = forms.DateTimeField(label="تاريخ الدخول", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    check_out_datetime = forms.DateTimeField(label="تاريخ الخروج", widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from .models import Apartment, Invoice
        active_apartment_ids = Invoice.objects.filter(
            check_out_datetime__gte=timezone.now()
        ).values_list('apartment_id', flat=True)

        choices = []
        for apt in Apartment.objects.all():
            label = f"{apt.name}"
            if apt.id in active_apartment_ids:
                label += " 🔴 (مؤجرة الآن)"
            choices.append((apt.id, label))

        self.fields['apartment'].choices = choices

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'custom_category', 'description', 'project_scope', 'is_recurring']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
