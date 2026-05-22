from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from students.models import Student


@login_required
def index(request):
    qs = Complaint.objects.select_related('student__user').all()
    q        = request.GET.get('q', '').strip()
    status   = request.GET.get('status', '')
    category = request.GET.get('category', '')
    priority = request.GET.get('priority', '')
    if q:
        qs = qs.filter(title__icontains=q) | \
             qs.filter(student__roll_number__icontains=q) | \
             qs.filter(student__user__first_name__icontains=q)
    if status:
        qs = qs.filter(status=status)
    if category:
        qs = qs.filter(category=category)
    if priority:
        qs = qs.filter(priority=priority)
    return render(request, 'complaints/index.html', {'complaints': qs})


@login_required
def detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/detail.html', {'complaint': complaint})


@login_required
def add(request):
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        student = get_object_or_404(Student, pk=p.get('student'))
        c = Complaint.objects.create(
            student        = student,
            title          = p.get('title'),
            complaint_text = p.get('complaint_text'),
            category       = p.get('category', 'OTHER'),
            priority       = p.get('priority', 'MEDIUM'),
            status         = 'PENDING',
        )
        if request.FILES.get('attachment'):
            c.attachment = request.FILES['attachment']
            c.save()
        messages.success(request, "Complaint filed successfully.")
        return redirect('complaints:detail', pk=c.pk)
    return render(request, 'complaints/form.html', {'action': 'Add', 'students': students})


@login_required
def edit(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    students = Student.objects.select_related('user').filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        complaint.student        = get_object_or_404(Student, pk=p.get('student'))
        complaint.title          = p.get('title', complaint.title)
        complaint.complaint_text = p.get('complaint_text', complaint.complaint_text)
        complaint.category       = p.get('category', complaint.category)
        complaint.priority       = p.get('priority', complaint.priority)
        complaint.status         = p.get('status', complaint.status)
        complaint.admin_response = p.get('admin_response', '')
        if request.FILES.get('attachment'):
            complaint.attachment = request.FILES['attachment']
        # Auto-set resolved fields
        if complaint.status == 'RESOLVED' and not complaint.resolved_at:
            from django.utils import timezone
            complaint.resolved_at = timezone.now()
            complaint.resolved_by = request.user
        complaint.save()
        messages.success(request, "Complaint updated.")
        return redirect('complaints:detail', pk=complaint.pk)
    return render(request, 'complaints/form.html', {
        'action': 'Edit', 'complaint': complaint, 'students': students
    })


@login_required
def delete(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, "Complaint deleted.")
        return redirect('complaints:index')
    return render(request, 'complaints/confirm_delete.html', {'complaint': complaint})
