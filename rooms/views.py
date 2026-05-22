from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room


@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/index.html', {'rooms': rooms})


@login_required
def detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    students = room.students.filter(is_active=True).select_related('user')
    return render(request, 'rooms/detail.html', {'room': room, 'students': students})


@login_required
def add(request):
    if request.method == 'POST':
        p = request.POST
        Room.objects.create(
            room_number  = p.get('room_number'),
            floor        = int(p.get('floor', 0)),
            room_type    = p.get('room_type', 'DOUBLE'),
            capacity     = int(p.get('capacity', 2)),
            monthly_rent = p.get('monthly_rent', 0),
            amenities    = p.get('amenities', ''),
            is_active    = bool(p.get('is_active')),
        )
        messages.success(request, "Room added successfully.")
        return redirect('rooms:index')
    return render(request, 'rooms/form.html', {'action': 'Add'})


@login_required
def edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        p = request.POST
        room.room_number  = p.get('room_number', room.room_number)
        room.floor        = int(p.get('floor', room.floor))
        room.room_type    = p.get('room_type', room.room_type)
        room.capacity     = int(p.get('capacity', room.capacity))
        room.monthly_rent = p.get('monthly_rent', room.monthly_rent)
        room.amenities    = p.get('amenities', '')
        room.is_active    = bool(p.get('is_active'))
        room.save()
        messages.success(request, "Room updated successfully.")
        return redirect('rooms:detail', pk=room.pk)
    return render(request, 'rooms/form.html', {'action': 'Edit', 'room': room})


@login_required
def delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted.")
        return redirect('rooms:index')
    return render(request, 'rooms/confirm_delete.html', {'room': room})
