# 02. Project Structure

> Penjelasan lengkap struktur folder dan file pada Employee Management System.

## 📋 Overview

Dokumen ini menjelaskan setiap folder dan file utama, fungsinya, serta best practice penamaan dan penempatan kode.

## 📁 Struktur Utama

```
employee_management/
├── apps/               # Django applications (business logic)
├── api/                # API layer (presentation)
├── config/             # Django settings & config
├── docs/               # Dokumentasi project
├── tests/              # Test suites
├── requirements/       # (Optional) Split requirements
├── scripts/            # Utility scripts
├── logs/               # Application logs (gitignored)
├── media/              # User uploads (gitignored)
├── static/             # Static files
├── .env.example        # Environment variables template
├── .gitignore
├── manage.py
└── README.md
```

## 📂 Penjelasan Folder

- **apps/**: Semua Django apps (core, accounts, employees, attendance, leave, approval, dst)
- **api/**: Layer API (shared, v1, dst)
- **config/**: Settings, urls, wsgi/asgi
- **docs/**: Semua dokumentasi project
- **tests/**: Test unit, integration, E2E
- **requirements/**: (Jika split requirements)
- **scripts/**: Script utilitas (backup, restore, dsb)
- **logs/**: Log aplikasi (jangan di-commit)
- **media/**: Upload user (jangan di-commit)
- **static/**: Static files (CSS, JS, images)

## 📄 Penjelasan File Penting

- **.env.example**: Template environment variables
- **.gitignore**: File/folder yang diabaikan git
- **manage.py**: Django management script
- **README.md**: Overview project & quick links

## 📝 Best Practices

- Satu app = satu domain bisnis
- Jangan campur logic API & business di satu folder
- Gunakan nama folder/file yang jelas & konsisten
- Pisahkan config, logic, dan presentasi

## 🔗 Lanjutkan ke:
- [03_development.md](03_development.md) - Development workflow
- [guides/README.md](guides/README.md) - Step-by-step development
