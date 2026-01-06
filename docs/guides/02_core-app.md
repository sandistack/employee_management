# README 02: Core App Foundation

## 📋 Overview

Pada tahap ini, kita akan membuat **Core App** yang berisi:
- Base models (TimeStamped, SoftDelete, Audit)
- Permission system (constants & groups)
- Utility functions (datetime, formatting)
- Management commands

---

## 🎯 Goals

Setelah menyelesaikan README ini, lo akan punya:

✅ Base models untuk inheritance  
✅ Permission constants untuk type-safety  
✅ Datetime & formatting helpers  
✅ Management command untuk setup groups  

---

## 📁 Structure Yang Akan Dibuat
```
apps/core/
├── constants/
│   ├── __init__.py              ← NEW
│   └── permission.py            ← NEW
├── models/
│   ├── __init__.py              ← NEW
│   ├── base.py                  ← NEW
│   └── permissions.py           ← NEW
├── utils/
│   ├── __init__.py              ← NEW
│   ├── datetime.py              ← NEW
│   └── formatting.py            ← NEW
└── management/
    └── commands/
        └── setup_permissions.py ← NEW
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Create Directories
```bash
# Di root project
cd apps/core

# Create directories
mkdir -p constants
mkdir -p models
mkdir -p utils
mkdir -p management/commands

# Verify structure
tree
```

---

### Step 2: Create Permission Constants

#### 2.1 Create `apps/core/constants/__init__.py`
```bash
# Create file
touch constants/__init__.py
```

Isi file dengan:
```python
"""
Core constants for the application.
"""
from .permission import PermissionCodes, PermissionGroups

__all__ = [
    'PermissionCodes',
    'PermissionGroups',
]
```

**✅ Checkpoint:** File created with 8 lines

---

#### 2.2 Create `apps/core/constants/permission.py`
```bash
touch constants/permission.py
```

Isi file dengan kode dari: [Link to GitHub Gist/Pastebin]

**Atau copy dari section ini:**

<details>
<summary>Click to expand full code (115 lines)</summary>

\`\`\`python
# apps/core/constants/permission.py
"""
Permission constants untuk avoid typos.
"""

class PermissionCodes:
    """Centralized permission codenames"""
    
    # CORE
    VIEW_COMPANY_DASHBOARD = 'core.view_company_dashboard'
    VIEW_DIVISION_DASHBOARD = 'core.view_division_dashboard'
    VIEW_OWN_DASHBOARD = 'core.view_own_dashboard'
    EXPORT_DASHBOARD_DATA = 'core.export_dashboard_data'
    VIEW_ANALYTICS = 'core.view_analytics'
    EXPORT_ATTENDANCE_REPORT = 'core.export_attendance_report'
    EXPORT_LEAVE_REPORT = 'core.export_leave_report'
    EXPORT_PAYROLL_REPORT = 'core.export_payroll_report'
    MANAGE_SYSTEM_SETTINGS = 'core.manage_system_settings'
    VIEW_AUDIT_LOGS = 'core.view_audit_logs'
    
    # ACCOUNTS.DIVISION
    ADD_DIVISION = 'accounts.add_division'
    CHANGE_DIVISION = 'accounts.change_division'
    DELETE_DIVISION = 'accounts.delete_division'
    VIEW_DIVISION = 'accounts.view_division'
    MANAGE_DIVISION_HIERARCHY = 'accounts.manage_division_hierarchy'
    VIEW_DIVISION_TREE = 'accounts.view_division_tree'
    BULK_IMPORT_DIVISIONS = 'accounts.bulk_import_divisions'
    EXPORT_DIVISION_DATA = 'accounts.export_division_data'
    
    # ACCOUNTS.USER
    ADD_USER = 'accounts.add_user'
    CHANGE_USER = 'accounts.change_user'
    DELETE_USER = 'accounts.delete_user'
    VIEW_USER = 'accounts.view_user'
    VIEW_ALL_EMPLOYEES = 'accounts.view_all_employees'
    VIEW_DIVISION_EMPLOYEES = 'accounts.view_division_employees'
    MANAGE_EMPLOYEE_FACE_DATA = 'accounts.manage_employee_face_data'
    BULK_IMPORT_EMPLOYEES = 'accounts.bulk_import_employees'
    EXPORT_EMPLOYEE_DATA = 'accounts.export_employee_data'


class PermissionGroups:
    """Pre-defined permission sets by role"""
    
    STAFF = [
        PermissionCodes.VIEW_OWN_DASHBOARD,
        PermissionCodes.VIEW_DIVISION,
    ]
    
    MANAGER = STAFF + [
        PermissionCodes.VIEW_DIVISION_DASHBOARD,
        PermissionCodes.VIEW_DIVISION_EMPLOYEES,
        PermissionCodes.VIEW_DIVISION_TREE,
        PermissionCodes.EXPORT_ATTENDANCE_REPORT,
    ]
    
    HR_ADMIN = MANAGER + [
        PermissionCodes.VIEW_COMPANY_DASHBOARD,
        PermissionCodes.EXPORT_DASHBOARD_DATA,
        PermissionCodes.ADD_DIVISION,
        PermissionCodes.CHANGE_DIVISION,
        PermissionCodes.DELETE_DIVISION,
        PermissionCodes.MANAGE_DIVISION_HIERARCHY,
        PermissionCodes.BULK_IMPORT_DIVISIONS,
        PermissionCodes.EXPORT_DIVISION_DATA,
        PermissionCodes.VIEW_ALL_EMPLOYEES,
        PermissionCodes.ADD_USER,
        PermissionCodes.CHANGE_USER,
        PermissionCodes.MANAGE_EMPLOYEE_FACE_DATA,
        PermissionCodes.BULK_IMPORT_EMPLOYEES,
        PermissionCodes.EXPORT_LEAVE_REPORT,
        PermissionCodes.EXPORT_PAYROLL_REPORT,
        PermissionCodes.VIEW_ANALYTICS,
    ]
\`\`\`

</details>

**✅ Checkpoint:** File created with ~115 lines

---

### Step 3: Create Base Models

Ikuti langkah yang sama untuk:

- `apps/core/models/__init__.py` (10 lines)
- `apps/core/models/base.py` (150 lines)
- `apps/core/models/permissions.py` (30 lines)

**Download all files:** [Link to ZIP/GitHub]

**Or follow individual steps below...**

---

### Step 4: Create Utility Functions

Files to create:
- `apps/core/utils/__init__.py`
- `apps/core/utils/datetime.py`
- `apps/core/utils/formatting.py`

**Download utils files:** [Link]

---

### Step 5: Create Management Command

File: `apps/core/management/commands/setup_permissions.py`

**Download:** [Link]

---

## ✅ Verification

### Test 1: Import Check
```bash
python manage.py shell
```
```python
# Should work without errors
from core.constants.permission import PermissionCodes
from core.models import AuditModel
from core.utils import now, format_datetime

print("✅ All imports successful!")
```

---

### Test 2: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected output:**
```
Migrations for 'core':
  core/migrations/0001_initial.py
    - Create model AppPermission
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying core.0001_initial... OK
```

---

### Test 3: Setup Permissions
```bash
python manage.py setup_permissions
```

**Expected output:**
```
Setting up groups and permissions...

✓ Created Staff group
✓ Created Manager group
✓ Created HR Admin group

Assigning permissions to Staff:
  ✓ view_own_dashboard
  ✓ view_division

Assigning permissions to Manager:
  ✓ view_own_dashboard
  ✓ view_division
  ✓ view_division_dashboard
  ...

✓ Setup complete!
```

---

### Test 4: Verify Groups Created
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import Group

groups = Group.objects.all()
print(groups)
# Output: <QuerySet [<Group: Staff>, <Group: Manager>, <Group: HR Admin>]>

# Check permissions
hr_admin = Group.objects.get(name='HR Admin')
print(hr_admin.permissions.count())
# Output: Should be > 15 permissions
```

---

## 📝 Full Code Download

Jika lo males copy satu-satu, download semua file sekaligus:

**Option 1: GitHub Gist**
```bash
# Download all files
curl -o core-files.zip https://gist.github.com/...
unzip core-files.zip -d apps/core/
```

**Option 2: Direct Copy**

Semua file ada di folder: `reference-code/02-core-app/`

Copy semua:
```bash
cp -r reference-code/02-core-app/* apps/core/
```

---

## 🐛 Troubleshooting

### Issue 1: Import Error

**Error:**
```
ImportError: cannot import name 'PermissionCodes'
```

**Solution:**
```bash
# Check file exists
ls apps/core/constants/permission.py

# Check __init__.py
cat apps/core/constants/__init__.py
```

---

### Issue 2: Migration Error

**Error:**
```
django.db.utils.OperationalError: no such table: core_apppermission
```

**Solution:**
```bash
# Run migrations
python manage.py makemigrations core
python manage.py migrate
```

---

### Issue 3: Permission Not Found

**Error:**
```
⚠ Permission not found: core.view_company_dashboard
```

**Solution:**
```bash
# Permissions created after migration
# Run migrate first, then setup_permissions
python manage.py migrate
python manage.py setup_permissions
```

---

## 🎯 Next Steps

**README 02 Complete! ✅**

Proceed to: **[README 03: Update Models to Use Core](./README-03-UPDATE-MODELS.md)**

In README 03, you'll:
- Update Division model to use AuditModel
- Update User model with audit fields
- Add custom permissions to models
- Test integration

---

## 📚 Reference

- Django Custom Permissions: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-permissions
- Django Model Inheritance: https://docs.djangoproject.com/en/4.2/topics/db/models/#model-inheritance
- Python datetime: https://docs.python.org/3/library/datetime.html

---

**Questions?** Review this README or check troubleshooting section.

**Ready?** Proceed to README 03! 🚀