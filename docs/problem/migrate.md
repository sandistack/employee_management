# Problem Migrate - Panduan Troubleshooting 🔧

## Daftar Isi
- [Problem Umum](#problem-umum)
- [Solusi Cepat](#solusi-cepat)
- [Skenario & Solusi](#skenario--solusi)
- [Command Penting](#command-penting)
- [Tips & Best Practice](#tips--best-practice)

---

## Problem Umum

### Kesalahan yang Sering Terjadi

| Error Message | Penyebab | Solusi Cepat |
|--------------|----------|--------------|
| `Table already exists` | Database sudah punya table, migration belum ditandai applied | `migrate app 0001 --fake` |
| `No such table` | Migration belum dijalankan | `migrate` (normal) |
| `Foreign key constraint failed` | Table dependency belum ada | `migrate` (Django handle otomatis) |
| `Column already exists` | Migration sudah pernah dijalankan manual | `migrate app 00XX --fake` |
| `Conflicting migrations` | Merge conflict di git | `makemigrations --merge` |

---

## Solusi Cepat

### 1. Table Sudah Ada, Migration Belum Applied

**Situasi:**
```bash
$ python manage.py migrate
django.db.utils.OperationalError: table "users" already exists
```

**Solusi:**
```bash
# 1. Cek status migration
$ python manage.py showmigrations accounts
accounts
 [ ] 0001_initial  # ← Table sudah ada, tapi migration belum ditandai
 [ ] 0002_add_phone

# 2. Fake migration yang table-nya sudah ada
$ python manage.py migrate accounts 0001_initial --fake

# 3. Cek lagi
$ python manage.py showmigrations accounts
accounts
 [X] 0001_initial  # ✅ Sudah ditandai
 [ ] 0002_add_phone

# 4. Apply sisanya (normal)
$ python manage.py migrate accounts
```

---

### 2. Table Belum Ada, Migration Ada

**Situasi:**
```bash
$ python manage.py runserver
django.db.utils.OperationalError: no such table: divisions
```

**Solusi:**
```bash
# Apply semua pending migrations
$ python manage.py migrate

# Django akan apply migrations sesuai dependency order
# Output:
Running migrations:
  Applying divisions.0001_initial... OK
  Applying accounts.0003_add_division... OK
```

---

### 3. Conflict Setelah Git Merge

**Situasi:**
```bash
# Developer A: 0004_add_phone.py
# Developer B: 0004_add_email.py
# Setelah merge: CONFLICT!
```

**Solusi:**
```bash
# 1. Selesaikan git conflict dulu (keep both files)

# 2. Buat merge migration
$ python manage.py makemigrations --merge

# Output:
Merging accounts
  Branch 0004_add_phone
  Branch 0004_add_email
Created new merge migration 0005_merge_20250107_1234.py

# 3. Apply merge migration
$ python manage.py migrate

# 4. Commit merge migration
$ git add apps/accounts/migrations/0005_merge_*.py
$ git commit -m "Merge conflicting migrations"
```

---

## Skenario & Solusi

### Skenario 1: Fresh Clone Project, Database Ada Data

**Problem:**
```
- Clone project dari git
- Database production/staging sudah ada data
- Running migrate = error "table already exists"
```

**Solusi:**
```bash
# JANGAN migrate biasa! ❌

# 1. Backup database dulu!
$ cp db.sqlite3 db.sqlite3.backup  # SQLite
# atau
$ pg_dump dbname > backup.sql      # PostgreSQL

# 2. Cek migration status
$ python manage.py showmigrations

# 3. Fake semua migration yang table-nya sudah ada
$ python manage.py migrate --fake

# 4. Atau fake per app sampai migration tertentu
$ python manage.py migrate accounts 0001 --fake
$ python manage.py migrate divisions 0001 --fake

# 5. Apply yang belum ada (normal)
$ python manage.py migrate
```

---

### Skenario 2: Developer Lain Tambah Model, Lokal Belum Ada Table

**Problem:**
```
- Git pull dapat migration baru
- Error: "Foreign key constraint" atau "no such table"
```

**Solusi:**
```bash
# 1. Pull code
$ git pull origin main

# 2. Cek migration baru
$ python manage.py showmigrations
accounts
 [X] 0001_initial
 [X] 0002_add_phone
 [ ] 0003_add_division  # ← Baru!
divisions
 [ ] 0001_initial       # ← Dependency!

# 3. Apply semua (Django handle dependency otomatis)
$ python manage.py migrate

# Output:
Running migrations:
  Applying divisions.0001_initial... OK
  Applying accounts.0003_add_division... OK
```

**Kalau masih error:**
```bash
# Lihat dependency tree
$ python manage.py showmigrations --plan

# Manual apply satu-satu
$ python manage.py migrate divisions
$ python manage.py migrate accounts
```

---

### Skenario 3: 0001_initial Error, Model Sudah Berubah

**Problem:**
```
- 0001_initial define schema lama
- models.py sudah berubah
- Database punya campuran old & new schema
```

**Solusi A: Development Only (NUCLEAR)**
```bash
# HANYA UNTUK DEVELOPMENT! DATA HILANG!

# 1. Backup data penting
$ python manage.py dumpdata accounts > accounts_backup.json

# 2. Drop database
$ rm db.sqlite3  # SQLite
# atau
$ python manage.py dbshell
sqlite> DROP TABLE accounts_user;
sqlite> DROP TABLE django_migrations;

# 3. Migrate dari awal
$ python manage.py migrate

# 4. Restore data (kalau bisa)
$ python manage.py loaddata accounts_backup.json
```

**Solusi B: Production (CAREFUL!)**
```bash
# 1. Backup database
$ pg_dump dbname > backup_$(date +%Y%m%d).sql

# 2. Analisa perbedaan
$ python manage.py sqlmigrate accounts 0002
# Lihat SQL yang akan dijalankan

# 3. Manual ALTER TABLE di dbshell
$ python manage.py dbshell
postgres=# ALTER TABLE users ADD COLUMN phone VARCHAR(15);
postgres=# \q

# 4. Fake migration yang sudah dijalankan manual
$ python manage.py migrate accounts 0002 --fake

# 5. Test
$ python manage.py runserver
```

---

### Skenario 4: Rollback Migration

**Problem:**
```
- Migration 0004 ada bug
- Mau rollback ke 0003
```

**Solusi:**
```bash
# 1. Cek current state
$ python manage.py showmigrations accounts
accounts
 [X] 0001_initial
 [X] 0002_add_phone
 [X] 0003_add_division
 [X] 0004_add_salary  # ← Mau di-rollback

# 2. Rollback ke 0003
$ python manage.py migrate accounts 0003

# Output:
Unapplying accounts.0004_add_salary... OK

# 3. Cek hasil
$ python manage.py showmigrations accounts
accounts
 [X] 0001_initial
 [X] 0002_add_phone
 [X] 0003_add_division
 [ ] 0004_add_salary  # ✅ Unapplied

# 4. Fix 0004_add_salary.py

# 5. Apply lagi
$ python manage.py migrate accounts
```

**Rollback semua migrations di app:**
```bash
# Rollback semua (DANGER: DROP ALL TABLES!)
$ python manage.py migrate accounts zero

# Cek
$ python manage.py showmigrations accounts
accounts
 [ ] 0001_initial
 [ ] 0002_add_phone
 [ ] 0003_add_division
 [ ] 0004_add_salary
```

---

### Skenario 5: Skip Migration Sementara

**Problem:**
```
- 0003 ada error
- Mau skip dulu, apply 0004
```

**Solusi (DANGEROUS!):**
```bash
# 1. Fake migration yang error
$ python manage.py migrate accounts 0003 --fake

# 2. Apply sisanya
$ python manage.py migrate accounts

# 3. Nanti fix 0003 dengan migration baru
$ python manage.py makemigrations --name fix_0003_issue
```

**Better solution:**
```bash
# Rollback, fix, reapply
$ python manage.py migrate accounts 0002
# Edit 0003_*.py
$ python manage.py migrate accounts
```

---

## Command Penting

### Show Migration Status

```bash
# Semua apps
$ python manage.py showmigrations

# App tertentu
$ python manage.py showmigrations accounts

# Dengan dependency tree
$ python manage.py showmigrations --plan
```

### Apply Migrations

```bash
# Apply semua pending
$ python manage.py migrate

# Apply app tertentu
$ python manage.py migrate accounts

# Apply sampai migration tertentu
$ python manage.py migrate accounts 0002

# Fake migration (mark sebagai applied tanpa run SQL)
$ python manage.py migrate accounts 0001 --fake

# Fake semua
$ python manage.py migrate --fake
```

### Rollback Migrations

```bash
# Rollback ke migration tertentu
$ python manage.py migrate accounts 0002

# Rollback semua migrations di app
$ python manage.py migrate accounts zero
```

### Debug Migrations

```bash
# Lihat SQL yang akan dijalankan
$ python manage.py sqlmigrate accounts 0002

# Output:
BEGIN;
ALTER TABLE "users" ADD COLUMN "phone" varchar(15) NOT NULL;
COMMIT;

# Check unapplied migrations (untuk CI/CD)
$ python manage.py migrate --check
```

### Create Migrations

```bash
# Auto-detect changes
$ python manage.py makemigrations

# Dengan nama custom
$ python manage.py makemigrations --name add_phone_field

# Merge conflicting migrations
$ python manage.py makemigrations --merge

# Empty migration (untuk RunPython)
$ python manage.py makemigrations --empty accounts
```

---

## Tips & Best Practice

### 1. Workflow Development

```bash
# Sebelum mulai kerja
$ git pull origin main
$ python manage.py migrate  # ✅ Selalu migrate dulu!
$ python manage.py runserver

# Setelah edit models.py
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py test

# Sebelum commit
$ git add apps/accounts/models.py
$ git add apps/accounts/migrations/0004_*.py  # ✅ Jangan lupa migrations!
$ git commit -m "Add phone field to User model"
```

### 2. Naming Convention

```bash
# ❌ Bad
$ python manage.py makemigrations
# Creates: 0004_auto_20250107_1234.py

# ✅ Good
$ python manage.py makemigrations --name add_phone_to_user
# Creates: 0004_add_phone_to_user.py
```

### 3. Testing Migrations

```bash
# Test forward
$ python manage.py migrate accounts 0004

# Test backward (rollback)
$ python manage.py migrate accounts 0003

# Test forward lagi
$ python manage.py migrate accounts 0004

# Kalau berhasil bolak-balik, baru commit!
```

### 4. Production Deployment

```bash
# Server production
$ git pull origin main

# Backup database dulu!
$ pg_dump dbname > backup_before_migration.sql

# Dry run - lihat SQL yang akan dijalankan
$ python manage.py sqlmigrate accounts 0004

# Apply migrations
$ python manage.py migrate

# Restart service
$ systemctl restart gunicorn
```

### 5. Cek Migration Sebelum Deploy

```bash
# Di local
$ python manage.py migrate --check
# Exit code 0 = tidak ada unapplied migrations
# Exit code 1 = ada unapplied migrations

# Good untuk CI/CD
if ! python manage.py migrate --check; then
    echo "⚠️  WARNING: Unapplied migrations detected!"
    exit 1
fi
```

### 6. Debugging Tips

```bash
# Lihat SQL query
$ python manage.py sqlmigrate accounts 0004

# Masuk ke database shell
$ python manage.py dbshell

# SQLite
sqlite> .schema users
sqlite> SELECT * FROM django_migrations WHERE app='accounts';

# PostgreSQL
postgres=# \d users
postgres=# SELECT * FROM django_migrations WHERE app='accounts';
```

### 7. Common Checks

| Check | Command |
|-------|---------|
| Ada unapplied migrations? | `showmigrations \| grep "\[ \]"` |
| Migration sudah applied? | `showmigrations accounts` |
| SQL apa yang akan dijalankan? | `sqlmigrate accounts 0004` |
| Dependency migration? | `showmigrations --plan` |

---

## Decision Tree: "Migration Saya Error, Apa Yang Harus Saya Lakukan?"

```
START: Migration Error
│
├─ Apakah ini production?
│  └─ YES → ⚠️  STOP! Backup dulu, konsultasi senior/DBA
│  └─ NO → Lanjut
│
├─ Apakah ada data penting?
│  └─ YES → Backup: python manage.py dumpdata > backup.json
│  └─ NO → Lanjut
│
├─ Error apa?
│  │
│  ├─ "Table already exists"
│  │  └─ migrate app 0001 --fake
│  │
│  ├─ "No such table"
│  │  └─ migrate (biasa)
│  │
│  ├─ "Foreign key constraint"
│  │  └─ migrate (Django handle dependency)
│  │
│  ├─ "Conflicting migrations"
│  │  └─ makemigrations --merge
│  │
│  ├─ "Column already exists"
│  │  └─ migrate app 00XX --fake
│  │
│  └─ "Everything broken!"
│     └─ Nuclear option (dev only):
│        1. rm db.sqlite3
│        2. python manage.py migrate
│        3. python manage.py loaddata backup.json
```

---

## Checklist: Sebelum Push Migrations

```bash
✅ [ ] Models.py sudah benar
✅ [ ] Sudah makemigrations
✅ [ ] Sudah migrate di local
✅ [ ] Test bisa rollback (migrate ke previous)
✅ [ ] Test bisa forward lagi (migrate ke latest)
✅ [ ] Test tidak ada data loss
✅ [ ] Migration file sudah di-add ke git
✅ [ ] Commit message jelas
```

---

## Checklist: Setelah Pull Migrations

```bash
✅ [ ] git pull origin main
✅ [ ] python manage.py showmigrations  # Cek ada pending
✅ [ ] python manage.py migrate         # Apply pending
✅ [ ] python manage.py test            # Run tests
✅ [ ] python manage.py runserver       # Test manual
```

---

## FAQ

### Q: Kapan pakai `--fake`?

**A:** Hanya ketika:
- Table/column sudah ada di database
- Tapi migration belum ditandai sebagai applied
- Biasanya karena database existing atau manual ALTER TABLE

### Q: Aman tidak pakai `--fake-initial`?

**A:** `--fake-initial` akan fake migration jika semua table-nya sudah ada. Lebih aman daripada `--fake` untuk initial migration.

```bash
$ python manage.py migrate --fake-initial
```

### Q: Gimana kalau --fake salah migration?

**A:** Rollback dan fix:

```bash
# 1. Rollback (unapply migration yang di-fake salah)
$ python manage.py migrate accounts 0002

# 2. Apply lagi dengan benar
$ python manage.py migrate accounts 0003
```

### Q: Boleh edit migration yang sudah applied?

**A:** ❌ JANGAN! Buat migration baru saja.

```bash
# ❌ Bad
# Edit 0003_add_phone.py (sudah applied)

# ✅ Good
$ python manage.py makemigrations --name fix_phone_field
# Creates new: 0004_fix_phone_field.py
```

### Q: Gimana hapus migration yang belum di-push?

**A:** Kalau belum di-push ke git dan belum shared ke tim:

```bash
# 1. Rollback migration
$ python manage.py migrate accounts 0002

# 2. Hapus file migration
$ rm apps/accounts/migrations/0003_*.py

# 3. Edit models.py sesuai kebutuhan

# 4. Buat migration baru
$ python manage.py makemigrations
```

### Q: Production migration error, apa yang dilakukan?

**A:** 

```bash
# 1. JANGAN PANIK!
# 2. Restore dari backup
$ psql dbname < backup_before_migration.sql

# 3. Rollback code ke commit sebelumnya
$ git revert HEAD
$ git push

# 4. Deploy ulang
$ git pull
$ systemctl restart gunicorn

# 5. Analisa masalah di local
# 6. Fix, test, baru deploy lagi
```

---

## Summary

### Golden Rules

1. **Selalu backup sebelum migrate**
2. **Test migration (forward & backward) sebelum push**
3. **Commit migrations bersamaan dengan models.py**
4. **Jangan edit migration yang sudah applied**
5. **--fake hanya untuk table yang sudah ada**
6. **Production: Extra careful, always backup!**

### Quick Commands

```bash
# Cek status
python manage.py showmigrations

# Apply normal
python manage.py migrate

# Apply ke migration tertentu
python manage.py migrate app_name 0002

# Fake (table sudah ada)
python manage.py migrate app_name 0001 --fake

# Rollback
python manage.py migrate app_name 0001

# Merge conflict
python manage.py makemigrations --merge

# Debug SQL
python manage.py sqlmigrate app_name 0002
```

---

**Terakhir Update:** Januari 2025  
**Versi:** 1.0

---

*Semoga migrations lancar! 🚀*