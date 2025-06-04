from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Building
from django.contrib.auth.decorators import login_required
from .forms import BuildingWithApartmentsForm
from .models import Apartment
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Building, Apartment
from django.shortcuts import render, get_object_or_404, redirect
from .models import Building, Apartment
from .forms import ApartmentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tenant
from .forms import TenantForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from .models import Invoice
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Tenant, Apartment, Invoice, Reservation, Rental
from .forms import InvoiceForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from .models import Expense, Payment
from .forms import ExpenseForm, PaymentForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # غيّر المسار حسب ما تبي
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # تشفير الباسورد
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def building_list(request):
    buildings = Building.objects.all().order_by('-id')
    return render(request, 'building_list.html', {'buildings': buildings})

@login_required
def building_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        counts = request.POST.getlist('count[]')
        rooms = request.POST.getlist('rooms[]')
        starts = request.POST.getlist('start_number[]')
        livings = request.POST.getlist('living[]')

        apartment_data = []
        total_apartments = 0

        for idx in range(len(counts)):
            try:
                count = int(counts[idx])
                room_count = int(rooms[idx])
                start = int(starts[idx])
            except (ValueError, IndexError):
                continue

            has_living_room = False
            if idx < len(livings):
                has_living_room = livings[idx].lower() == 'yes'

            for i in range(count):
                apartment_data.append({
                    "number": start + i,
                    "room_count": room_count,
                    "has_living_room": has_living_room
                })
                total_apartments += 1

        if total_apartments == 0:
            messages.error(request, "يجب إدخال تفاصيل شقة واحدة على الأقل.")
            return render(request, 'building_create.html')

        building = Building.objects.create(
            name=name,
            apartment_count=total_apartments
        )

        for apt in apartment_data:
            Apartment.objects.create(
                building=building,
                name=f"{name} - {apt['number']}",
                room_count=apt["room_count"],
                has_living_room=apt["has_living_room"]
            )

        messages.success(request, f"تم إنشاء العمارة '{name}' بنجاح مع {total_apartments} شقة.")
        return redirect('building_list')

    return render(request, 'building_create.html')

@login_required
def delete_building(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    if request.method == 'POST':
        building.delete()
        messages.success(request, f"تم حذف العمارة '{building.name}' بنجاح.")
        return redirect('building_list')

@login_required
def edit_building(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    apartments = Apartment.objects.filter(building=building)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        to_delete = request.POST.getlist('delete_apartments[]')

        if new_name and new_name != building.name:
            building.name = new_name
            building.save()

        if to_delete:
            Apartment.objects.filter(id__in=to_delete, building=building).delete()

        building.apartment_count = Apartment.objects.filter(building=building).count()
        building.save()

        messages.success(request, "تم تحديث بيانات العمارة بنجاح.")
        return redirect('building_list')

    return render(request, 'edit_building.html', {
        'building': building,
        'apartments': apartments,
    })

from .models import Apartment

@login_required
def view_all_apartments(request):
    apartments = Apartment.objects.select_related('building').order_by('building__name', 'name')
    return render(request, 'view_all_apartments.html', {'apartments': apartments})

@login_required
def add_apartment(request, building_id):
    building = get_object_or_404(Building, id=building_id)

    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            room_count = form.cleaned_data['room_count']
            has_living_room = form.cleaned_data['has_living_room']

            apartment_name = f"{building.name} - {number}"

            if Apartment.objects.filter(name=apartment_name).exists():
                form.add_error('number', "رقم الشقة هذا موجود مسبقًا في هذه العمارة.")
            else:
                Apartment.objects.create(
                    building=building,
                    name=apartment_name,
                    room_count=room_count,
                    has_living_room=has_living_room
                )

                building.apartment_count += 1
                building.save()

                messages.success(request, f"تمت إضافة الشقة بنجاح إلى العمارة '{building.name}'")
                return redirect('building_list')
    else:
        form = ApartmentForm()

    return render(request, 'add_apartment.html', {'form': form, 'building': building})

@login_required
def tenant_list(request):
    tenants = Tenant.objects.all().order_by('-created_at')
    return render(request, 'tenant_list.html', {'tenants': tenants})

@login_required
def add_tenant(request):
    form = TenantForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tenant = form.save(commit=False)
        tenant.user = request.user
        tenant.save()
        messages.success(request, "تمت إضافة المستأجر بنجاح.")
        return redirect('tenant_list')
    return render(request, 'tenant_form.html', {'form': form, 'title': 'إضافة مستأجر'})

@login_required
def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    form = TenantForm(request.POST or None, instance=tenant)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "تم تحديث بيانات المستأجر بنجاح.")
        return redirect('tenant_list')
    return render(request, 'tenant_form.html', {'form': form, 'title': 'تعديل مستأجر'})

@login_required
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        messages.success(request, "تم حذف المستأجر.")
        return redirect('tenant_list')
    return render(request, 'tenant_confirm_delete.html', {'tenant': tenant})

from django.db.models import Q

def invoice_list(request):
    today = timezone.now().date()

    start_date = request.GET.get('start_date', today.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', today.strftime('%Y-%m-%d'))

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # ✅ نجلب الفواتير من أحد حالتين:
    invoices = Invoice.objects.filter(
        Q(created_at__date__range=(start, end)) |
        Q(payments__paid_at__date__range=(start, end))
    ).distinct()

    total_amount = sum(i.amount for i in invoices)
    total_paid = sum(i.total_paid for i in invoices)

    context = {
        'invoices': invoices,
        'start_date': start_date,
        'end_date': end_date,
        'total_amount': total_amount,
        'total_paid': total_paid,
    }
    return render(request, 'invoice_list.html', context)

@login_required
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            tenant_name = form.cleaned_data['tenant_name']
            tenant_phone = form.cleaned_data['tenant_phone']
            apartment = form.cleaned_data['apartment']
            amount = form.cleaned_data['amount']
            amount_paid = form.cleaned_data.get('amount_paid', 0)
            rent_type = form.cleaned_data['rent_type']
            check_in = form.cleaned_data['check_in_datetime']
            check_out = form.cleaned_data['check_out_datetime']

            tenant, _ = Tenant.objects.get_or_create(
                phone_number=tenant_phone,
                defaults={'name': tenant_name, 'user': request.user}
            )

            invoice = Invoice.objects.create(
                user=request.user,
                building=apartment.building,
                apartment=apartment,
                tenant=tenant,
                amount=amount,
                rent_type=rent_type,
                check_in_datetime=check_in,
                check_out_datetime=check_out
            )

            if amount_paid > 0:
                Payment.objects.create(
                    invoice=invoice,
                    amount=amount_paid,
                    added_by=request.user
                )

            messages.success(request, "تم إنشاء الفاتورة بنجاح.")
            return redirect('invoice_list')
    else:
        form = InvoiceForm()

    return render(request, 'add_invoice.html', {'form': form})

@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    tenant = invoice.tenant

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            tenant.name = form.cleaned_data['tenant_name']
            tenant.phone_number = form.cleaned_data['tenant_phone']
            tenant.save()

            apartment = form.cleaned_data['apartment']
            invoice.apartment = apartment
            invoice.building = apartment.building
            invoice.amount = form.cleaned_data['amount']
            invoice.rent_type = form.cleaned_data['rent_type']
            invoice.check_in_datetime = form.cleaned_data['check_in_datetime']
            invoice.check_out_datetime = form.cleaned_data['check_out_datetime']
            invoice.save()

            messages.success(request, "تم تعديل الفاتورة بنجاح.")
            return redirect('invoice_list')
    else:
        form = InvoiceForm(initial={
            'tenant_name': tenant.name,
            'tenant_phone': tenant.phone_number,
            'apartment': invoice.apartment,
            'amount': invoice.amount,
            'rent_type': invoice.rent_type,
            'check_in_datetime': invoice.check_in_datetime,
            'check_out_datetime': invoice.check_out_datetime,
        })

    return render(request, 'edit_invoice.html', {'form': form, 'invoice': invoice})

@require_POST
@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # حذف السجلات المرتبطة أولًا (اختياري لأننا حاطين on_delete=CASCADE)
    Reservation.objects.filter(invoice=invoice).delete()
    Rental.objects.filter(invoice=invoice).delete()

    invoice.delete()
    messages.success(request, "تم حذف الفاتورة بنجاح.")
    return redirect('invoice_list')

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_detail.html', {'invoice': invoice})

@login_required
def expense_list(request):
    filter_option = request.GET.get('filter')
    expenses = Expense.objects.filter(user=request.user)

    if filter_option == 'related':
        expenses = expenses.filter(project_scope='related')
    elif filter_option == 'unrelated':
        expenses = expenses.filter(project_scope='unrelated')
    elif filter_option == 'utilities':
        expenses = expenses.filter(category__in=['electricity', 'water'])
    elif filter_option == 'salary':
        expenses = expenses.filter(category='salary')
    elif filter_option == 'rent':
        expenses = expenses.filter(category='rent')
    elif filter_option == 'other':
        expenses = expenses.filter(category='other')

    expenses = expenses.order_by('-created_at')
    total = sum(e.amount for e in expenses)
    all_expenses = Expense.objects.filter(user=request.user)
    total_related = sum(e.amount for e in all_expenses if e.project_scope == 'related')
    total_unrelated = sum(e.amount for e in all_expenses if e.project_scope == 'unrelated')

    context = {
        'expenses': expenses,
        'total': total,
        'total_related': total_related,
        'total_unrelated': total_unrelated,
    }
    return render(request, 'expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('expense_list')

@login_required
def add_payment(request):
    invoice_id = request.GET.get('invoice_id')
    initial_data = {'invoice': invoice_id} if invoice_id else None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            invoice = form.cleaned_data['invoice']
            amount = form.cleaned_data['amount']

            Payment.objects.create(
                invoice=invoice,
                amount=amount,
                added_by=request.user
            )

            messages.success(request, f"تم تسجيل دفعة بقيمة {amount} ريال.")
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = PaymentForm(initial=initial_data)

    return render(request, 'add_payment.html', {'form': form})

@login_required
def daily_payments(request):
    from datetime import datetime
    from django.utils import timezone

    today = timezone.now().date()
    start_date = request.GET.get('start_date', today.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', today.strftime('%Y-%m-%d'))

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    payments = Payment.objects.filter(paid_at__date__gte=start, paid_at__date__lte=end)

    total_paid = sum(p.amount for p in payments)

    context = {
        'payments': payments,
        'total_paid': total_paid,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'daily_payments.html', context)