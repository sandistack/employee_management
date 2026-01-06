# 04. Database Guide

> Penjelasan schema database, ERD, dan strategi migrasi.

## 📋 Overview

Dokumen ini menjelaskan struktur database, relasi antar tabel, dan best practice migrasi.

## 🗄️ Database Schema

- **PostgreSQL** untuk production
- **SQLite** untuk development/testing

## 🗺️ ERD (Entity Relationship Diagram)

(Diagram/gambar bisa ditambahkan di sini)

## 🔄 Migrations

- Gunakan Django migrations
- Jangan edit tabel manual di DB
- Selalu jalankan `makemigrations` sebelum `migrate`

## 📝 Lanjutkan ke:
- [05_api.md](05_api.md) - API documentation
- [guides/README.md](guides/README.md) - Step-by-step development
