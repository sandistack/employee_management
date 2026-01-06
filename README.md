# Employee Management System

> Sistem manajemen karyawan internal dengan fitur absensi face recognition, cuti, dan approval matrix.

## 📋 Overview

Aplikasi ini dibuat untuk mengelola:
- ✅ Data karyawan (CRUD)
- ✅ Absensi menggunakan Face Recognition
- ✅ Pengajuan dan persetujuan cuti
- ✅ Multi-level approval matrix
- ✅ Dashboard admin dan staff

## 🚀 Quick Start

**Just want to run the project?** Follow: **[Installation Guide](docs/01_installation.md)**

```bash
# Clone repository
git clone <repository-url> employee_management
cd employee_management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit: http://127.0.0.1:8000/admin/

## 📚 Documentation

### For Users/Developers
| Dokumen | Deskripsi |
|---------|-----------|
| [Installation Guide](docs/01_installation.md) | Install project dari Git repository |
| [Project Structure](docs/02_structure.md) | Penjelasan struktur folder & conventions |
| [API Documentation](docs/05_api.md) | RESTful API endpoints reference |
| [Testing Guide](docs/06_testing.md) | Running tests & coverage |
| [Deployment Guide](docs/07_deployment.md) | Deploy ke production server |

### For Learning/Building from Scratch
| Dokumen | Deskripsi |
|---------|-----------|
| [Development Guides](docs/guides/README.md) | **START HERE** - Step-by-step tutorials |
| [Setup from Scratch](docs/01_setup_from_scratch.md) | Build project dari NOL (advanced) |
| [Requirements Management](docs/notes/requirements.md) | Dependencies best practices |

## 🛠️ Tech Stack

- **Framework**: Django 5.0
- **API**: Django REST Framework 3.14
- **Database**: PostgreSQL 14+
- **Face Recognition**: face_recognition, OpenCV
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Testing**: pytest, pytest-django
- **Code Quality**: black, flake8, isort, pre-commit

## 🏗️ Project Structure
```
employee_management/
├── apps/               # Django applications (business logic)
│   ├── core/          # Base models, mixins, validators
│   ├── accounts/      # Custom user & authentication
│   ├── employees/     # Employee management
│   ├── attendance/    # Attendance & face recognition
│   ├── leave/         # Leave management
│   └── approval/      # Approval matrix
│
├── api/               # API layer (presentation)
│   ├── shared/        # Public endpoints (dropdown, etc)
│   └── v1/           # API version 1
│
├── config/            # Django settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
│
├── docs/              # Documentation
├── tests/             # Test suites
├── requirements/      # Dependencies
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
│
├── scripts/           # Utility scripts
├── logs/              # Application logs (gitignored)
├── media/             # User uploads (gitignored)
├── static/            # Static files
│
├── .env.example       # Environment variables template
├── .gitignore
├── manage.py
├── pytest.ini
└── README.md
```

## 🎯 Features

### Phase 1 ✅ (In Progress)
- [x] Project setup & documentation
- [ ] Custom User model
- [ ] Core app dengan base models
- [ ] Employee CRUD
- [ ] Django Admin setup

### Phase 2 🚧 (Planned)
- [ ] API v1 setup
- [ ] Employee API endpoints
- [ ] JWT Authentication
- [ ] Permission system

### Phase 3 📅 (Planned)
- [ ] Attendance model
- [ ] Face recognition integration
- [ ] Check-in/out API
- [ ] Attendance history

### Phase 4 📅 (Planned)
- [ ] Leave management
- [ ] Approval matrix
- [ ] Multi-level approval flow

### Phase 5 📅 (Planned)
- [ ] Testing coverage
- [ ] Complete documentation
- [ ] Deployment preparation

## 🧪 Testing
```bash
# Run all tests
pytest

# Run dengan coverage
pytest --cov=apps --cov-report=html

# Run specific app
pytest tests/unit/test_employees.py
```

## 🤝 Development Workflow

Lihat [docs/03_development.md](docs/03_development.md) untuk:
- Git branching strategy
- Cara buat fitur baru
- Code review process
- Naming conventions

## 📝 Environment Variables

Copy `.env.example` ke `.env` dan sesuaikan:
```bash
cp .env.example .env
nano .env
```

## 👥 Team & Contact

- **Developer**: [Your Name]
- **Company**: [Company Name]
- **Started**: January 2026

## � License

Internal use only - Proprietary

---

**New to this project?**  
→ Start with: [Installation Guide](docs/01_installation.md)

**Want to learn Django & build from scratch?**  
→ Start with: [Development Guides](docs/guides/README.md)
