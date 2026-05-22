<img src="https://img.shields.io/badge/status-in%20progress-yellow" height="35">
# 🏠 Hostel Management System
A Django-based backend for managing hostel operations.

---

## 📁 Project Structure

```
hostel_management/           ← Project root
├── manage.py                ← Django command-line utility
├── db.sqlite3               ← SQLite database (auto-created)
├── README.md                ← This file
│
├── hostel_management/       ← Core Django config package
│   ├── settings.py          ← All configurations
│   ├── urls.py              ← Root URL dispatcher
│   ├── wsgi.py              ← WSGI entry point (production)
│   └── asgi.py              ← ASGI entry point (async)
│
├── authentication/          ← Login, logout, register
│   ├── views.py             ← register, profile, change_password
│   └── urls.py              ← /auth/login|logout|register|profile
│
├── students/                ← Student profiles
│   ├── models.py            ← Student model (links to User + Room)
│   ├── forms.py             ← UserForm + StudentForm
│   ├── views.py             ← CRUD views
│   └── urls.py              ← /students/
│
├── rooms/                   ← Room allocation
│   ├── models.py            ← Room model (capacity, floor, type)
│   ├── forms.py             ← RoomForm
│   ├── views.py             ← CRUD views
│   └── urls.py              ← /rooms/
│
├── fees/                    ← Fee management
│   ├── models.py            ← Fee model (amount, status, month)
│   ├── forms.py             ← FeeForm
│   ├── views.py             ← CRUD views
│   └── urls.py              ← /fees/
│
├── complaints/              ← Complaint tracking
│   ├── models.py            ← Complaint model (category, status)
│   ├── forms.py             ← ComplaintForm + ComplaintResponseForm
│   ├── views.py             ← CRUD views
│   └── urls.py              ← /complaints/
│
├── visitors/                ← Visitor log
│   ├── models.py            ← Visitor model (entry/exit times)
│   ├── forms.py             ← VisitorForm
│   ├── views.py             ← CRUD views
│   └── urls.py              ← /visitors/
│
├── dashboard/               ← Stats overview
│   ├── views.py             ← Aggregates data from all apps
│   └── urls.py              ← /dashboard/
│
├── templates/               ← All HTML templates
│   ├── base.html            ← Base layout (navbar, messages)
│   ├── authentication/      ← login.html, register.html
│   ├── students/            ← index, detail, form, confirm_delete
│   ├── rooms/
│   ├── fees/
│   ├── complaints/
│   ├── visitors/
│   └── dashboard/
│
├── static/                  ← CSS, JS, images (dev)
│   └── css/style.css
│
└── media/                   ← User uploads (profile pics, attachments)
    ├── students/profile_pics/
    └── complaints/attachments/
```

---

## 🗄️ Model Relationships

```
User (Django built-in)
 └── OneToOne ──► Student
                   ├── ForeignKey ──► Room
                   ├── Reverse ─────► Fee (many)
                   ├── Reverse ─────► Complaint (many)
                   └── Reverse ─────► Visitor (many)
```

---

## ⚡ Setup Commands (Run in Order)

```bash
# 1. Clone / enter project
cd hostel_management

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django pillow

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (admin panel access)
python manage.py createsuperuser
# Enter: username, email, password when prompted

# 6. Start development server
python manage.py runserver
```

---

## 🌐 URL Map

| URL                    | Module         | Description              |
|------------------------|----------------|--------------------------|
| `/`                    | —              | Redirects to dashboard   |
| `/admin/`              | Django Admin   | Full admin panel         |
| `/auth/login/`         | authentication | Login page               |
| `/auth/logout/`        | authentication | Logout                   |
| `/auth/register/`      | authentication | New user registration    |
| `/auth/profile/`       | authentication | View your profile        |
| `/dashboard/`          | dashboard      | Stats overview           |
| `/students/`           | students       | List all students        |
| `/students/<id>/`      | students       | Student detail           |
| `/students/add/`       | students       | Add new student          |
| `/students/<id>/edit/` | students       | Edit student             |
| `/rooms/`              | rooms          | List all rooms           |
| `/fees/`               | fees           | List all fees            |
| `/complaints/`         | complaints     | List all complaints      |
| `/visitors/`           | visitors       | Visitor log              |

---

## 🔐 Default Admin Credentials

```
URL:      http://127.0.0.1:8000/admin/
Username: admin
Password: admin1234
```
> Change these in production!

---

## 🔑 Key Django Concepts Used

| Concept | Where Used |
|---|---|
| `OneToOneField` | Student ↔ User |
| `ForeignKey` | Student → Room, Fee → Student, etc. |
| `related_name` | `room.students.all()`, `student.fees.all()` |
| `@login_required` | All views are protected |
| `ModelForm` | All `forms.py` files |
| `admin.TabularInline` | Students shown inside Room admin |
| `auto_now_add` | `created_at` timestamps |
| `select_related` | Efficient DB queries in views |
| `get_object_or_404` | Safe record fetching in views |
| `messages` framework | Success/error flash messages |

