from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Visitor
from students.models import Student


@login_required
def index(request):
    qs = Visitor.objects.select_related('student__user').all()
    q        = request.GET.get('q', '').strip()
    relation = request.GET.get('relation', '')
    inside   = request.GET.get('inside', '')
    if q:
        qs = qs.filter(visitor_name__icontains=q) | \
             qs.filter(student__roll_number__icontains=q) | \
             qs.filter(student__user__first_name__icontains=q)
    if relation:
        qs = qs.filter(relation=relation)
    if inside == '1':
        qs = qs.filter(exit_time__isnull=True)
    elif inside == '0':
        qs = qs.filter(exit_time__isnull=False)
    return render(request, 'visitors/index.html', {'visitors': qs})


@login_required
def detail(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    # Handle quick "Log Exit" POST from detail page
    if request.method == 'POST' and request.POST.get('log_exit'):
        visitor.record_exit()
        messages.success(request, f"Exit recorded for {visitor.visitor_name}.")
        return redirect('visitors:detail', pk=visitor.pk)
    return render(request, 'visitors/detail.html', {'visitor': visitor})


@login_required
def add(request):
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        student = get_object_or_404(Student, pk=p.get('student'))
        Visitor.objects.create(
            student         = student,
            visitor_name    = p.get('visitor_name'),
            visitor_phone   = p.get('visitor_phone', ''),
            relation        = p.get('relation', 'OTHER'),
            purpose         = p.get('purpose', ''),
            id_proof_type   = p.get('id_proof_type', 'CNIC'),
            id_proof_number = p.get('id_proof_number', ''),
            entry_time      = p.get('entry_time') or timezone.now(),
            exit_time       = p.get('exit_time') or None,
            approved_by     = p.get('approved_by', ''),
            notes           = p.get('notes', ''),
        )
        messages.success(request, "Visitor entry logged successfully.")
        return redirect('visitors:index')
    return render(request, 'visitors/form.html', {'action': 'Add', 'students': students})


@login_required
def edit(request, pk):
    visitor  = get_object_or_404(Visitor, pk=pk)
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        visitor.student         = get_object_or_404(Student, pk=p.get('student'))
        visitor.visitor_name    = p.get('visitor_name', visitor.visitor_name)
        visitor.visitor_phone   = p.get('visitor_phone', '')
        visitor.relation        = p.get('relation', visitor.relation)
        visitor.purpose         = p.get('purpose', '')
        visitor.id_proof_type   = p.get('id_proof_type', visitor.id_proof_type)
        visitor.id_proof_number = p.get('id_proof_number', '')
        visitor.entry_time      = p.get('entry_time') or visitor.entry_time
        visitor.exit_time       = p.get('exit_time') or None
        visitor.approved_by     = p.get('approved_by', '')
        visitor.notes           = p.get('notes', '')
        visitor.save()
        messages.success(request, "Visitor record updated.")
        return redirect('visitors:detail', pk=visitor.pk)
    return render(request, 'visitors/form.html', {
        'action': 'Edit', 'visitor': visitor, 'students': students
    })


@login_required
def delete(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if request.method == 'POST':
        visitor.delete()
        messages.success(request, "Visitor record deleted.")
        return redirect('visitors:index')
    return render(request, 'visitors/confirm_delete.html', {'visitor': visitor})
