from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student
from rooms.models import Room


@login_required
def index(request):
    qs = Student.objects.select_related('user', 'room').all()
    q    = request.GET.get('q', '').strip()
    dept = request.GET.get('dept', '')
    status = request.GET.get('status', '')
    if q:
        qs = qs.filter(
            roll_number__icontains=q
        ) | qs.filter(user__first_name__icontains=q) | qs.filter(user__last_name__icontains=q)
    if dept:
        qs = qs.filter(department=dept)
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'inactive':
        qs = qs.filter(is_active=False)
    return render(request, 'students/index.html', {'students': qs})


@login_required
def detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})


@login_required
def add(request):
    rooms = Room.objects.filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        # Validate passwords match
        if p.get('password1') != p.get('password2'):
            messages.error(request, "Passwords do not match.")
            return render(request, 'students/form.html', {'action': 'Add', 'rooms': rooms})
        if User.objects.filter(username=p.get('username')).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'students/form.html', {'action': 'Add', 'rooms': rooms})
        user = User.objects.create_user(
            username=p.get('username'),
            password=p.get('password1'),
            email=p.get('email', ''),
            first_name=p.get('first_name', ''),
            last_name=p.get('last_name', ''),
        )
        room = Room.objects.filter(pk=p.get('room')).first() if p.get('room') else None
        student = Student.objects.create(
            user=user,
            roll_number=p.get('roll_number'),
            department=p.get('department'),
            phone_number=p.get('phone_number'),
            room=room,
            guardian_name=p.get('guardian_name', ''),
            guardian_phone=p.get('guardian_phone', ''),
            address=p.get('address', ''),
            is_active=bool(p.get('is_active')),
        )
        if request.FILES.get('profile_pic'):
            student.profile_pic = request.FILES['profile_pic']
            student.save()
        messages.success(request, f"Student {student} added successfully.")
        return redirect('students:detail', pk=student.pk)
    return render(request, 'students/form.html', {'action': 'Add', 'rooms': rooms})


@login_required
def edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    rooms = Room.objects.filter(is_active=True)
    if request.method == 'POST':
        p = request.POST
        user = student.user
        user.first_name = p.get('first_name', '')
        user.last_name  = p.get('last_name', '')
        user.email      = p.get('email', '')
        user.save()
        room = Room.objects.filter(pk=p.get('room')).first() if p.get('room') else None
        student.roll_number   = p.get('roll_number', student.roll_number)
        student.department    = p.get('department', student.department)
        student.phone_number  = p.get('phone_number', student.phone_number)
        student.room          = room
        student.guardian_name = p.get('guardian_name', '')
        student.guardian_phone= p.get('guardian_phone', '')
        student.address       = p.get('address', '')
        student.is_active     = bool(p.get('is_active'))
        if request.FILES.get('profile_pic'):
            student.profile_pic = request.FILES['profile_pic']
        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect('students:detail', pk=student.pk)
    return render(request, 'students/form.html', {'action': 'Edit', 'student': student, 'rooms': rooms})


@login_required
def delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.delete()   # cascades to student
        messages.success(request, "Student deleted.")
        return redirect('students:index')
    return render(request, 'students/confirm_delete.html', {'student': student})
