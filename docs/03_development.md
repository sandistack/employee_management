# 03. Development Guide

> Panduan workflow development, branching, code style, dan review.

## 📋 Overview

Dokumen ini menjelaskan cara kerja tim, workflow git, code style, dan proses review.

## 🚦 Workflow Development

1. **Buat branch baru** untuk setiap fitur/bugfix
2. **Commit kecil & jelas**
3. **Push ke remote**
4. **Buat Pull Request (PR)**
5. **Code review & testing**
6. **Merge ke main/develop**

## 🌳 Branching Strategy

- `main`: Production-ready
- `develop`: Integrasi fitur sebelum ke main
- `feature/*`: Fitur baru
- `bugfix/*`: Perbaikan bug
- `hotfix/*`: Patch urgent

## 🧹 Code Style

- Gunakan black, flake8, isort
- Ikuti PEP8
- Tulis docstring & type hints

## 🔍 Review Process

- PR harus lulus CI & test
- Minimal 1 reviewer approve
- Diskusi di PR, bukan chat pribadi

## 📝 Lanjutkan ke:
- [04_database.md](04_database.md) - Database schema & migrations
- [guides/README.md](guides/README.md) - Step-by-step development
