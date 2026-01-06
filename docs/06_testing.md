# 06. Testing Guide

> Panduan testing: unit, integration, coverage, dan tools.

## 📋 Overview

Dokumen ini menjelaskan strategi testing, tools yang digunakan, dan cara menjalankan test.

## 🧪 Jenis Testing

- **Unit test**: Test fungsi/model terpisah
- **Integration test**: Test beberapa komponen bersama
- **E2E test**: Test flow aplikasi end-to-end

## 🛠️ Tools

- pytest
- pytest-django
- coverage.py

## 🚀 Menjalankan Test

```bash
pytest
pytest --cov=apps --cov-report=html
```

## 📝 Lanjutkan ke:
- [07_deployment.md](07_deployment.md) - Deployment guide
- [guides/README.md](guides/README.md) - Step-by-step development
