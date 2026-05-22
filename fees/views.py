from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fee
from students.models import Student


@login_required
def index(request):
    qs = Fee.objects.select_related('student__user').all()
    q      = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    ftype  = request.GET.get('type', '')
    if q:
        qs = qs.filter(student__roll_number__icontains=q) | \
             qs.filter(student__user__first_name__icontains=q) | \
             qs.filter(student__user__last_name__icontains=q)
    if status:
        qs = qs.filter(status=status)
    if ftype:
        qs = qs.filter(fee_type=ftype)
    return render(request, 'fees/index.html', {'fees': qs})


@login_required
def detail(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    return render(request, 'fees/detail.html', {'fee': fee})


@login_required
def add(request):
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        student = get_object_or_404(Student, pk=p.get('student'))
        Fee.objects.create(
            student      = student,
            fee_type     = p.get('fee_type', 'ROOM'),
            amount       = p.get('amount', 0),
            paid_amount  = p.get('paid_amount', 0),
            status       = p.get('status', 'PENDING'),
            month        = int(p.get('month', 1)),
            year         = int(p.get('year', 2025)),
            due_date     = p.get('due_date'),
            payment_date = p.get('payment_date') or None,
            remarks      = p.get('remarks', ''),
        )
        messages.success(request, "Fee record created.")
        return redirect('fees:index')
    return render(request, 'fees/form.html', {'action': 'Add', 'students': students})


@login_required
def edit(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        fee.student      = get_object_or_404(Student, pk=p.get('student'))
        fee.fee_type     = p.get('fee_type', fee.fee_type)
        fee.amount       = p.get('amount', fee.amount)
        fee.paid_amount  = p.get('paid_amount', fee.paid_amount)
        fee.status       = p.get('status', fee.status)
        fee.month        = int(p.get('month', fee.month))
        fee.year         = int(p.get('year', fee.year))
        fee.due_date     = p.get('due_date', fee.due_date)
        fee.payment_date = p.get('payment_date') or None
        fee.remarks      = p.get('remarks', '')
        fee.save()
        messages.success(request, "Fee record updated.")
        return redirect('fees:detail', pk=fee.pk)
    return render(request, 'fees/form.html', {'action': 'Edit', 'fee': fee, 'students': students})


@login_required
def delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, "Fee record deleted.")
        return redirect('fees:index')
    return render(request, 'fees/confirm_delete.html', {'fee': fee})
