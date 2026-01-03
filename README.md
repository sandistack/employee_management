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

**⚠️ PENTING: Baca dokumentasi setup lengkap di [docs/01_setup.md](docs/01_setup.md)**
```bash
# Clone repository
git clone 
cd employee_management

# Ikuti langkah-langkah di docs/01_setup.md
```

## 📚 Documentation

| Dokumen | Deskripsi |
|---------|-----------|
| [Setup Guide](docs/01_setup.md) | Instalasi & setup dari NOL |
| [Project Structure](docs/02_structure.md) | Penjelasan struktur folder |
| [Development Guide](docs/03_development.md) | Workflow development |
| [Database Guide](docs/04_database.md) | Database schema & migrations |
| [API Documentation](docs/05_api.md) | RESTful API endpoints |
| [Testing Guide](docs/06_testing.md) | Testing strategy & commands |
| [Deployment Guide](docs/07_deployment.md) | Deploy ke production |

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

## 📄 License

Internal use only - Proprietary

---

**🚀 Mulai dari [docs/01_setup.md](docs/01_setup.md)**
