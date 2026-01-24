# ============================================
# GUIDE: Multiple API Versions (v1, v2, v3)
# ============================================
# Kapan perlu API versioning v2?
# - Breaking changes (field dihapus/diganti)
# - Major changes di response format
# - Perlu support old clients

# ============================================
# STRUKTUR PROJECT
# ============================================

"""
api/
├── __init__.py
├── urls.py           # Main API routing
├── v1/               # Version 1 (current)
│   ├── __init__.py
│   ├── urls.py
│   └── accounts/
│       ├── serializers/
│       ├── viewsets/
│       └── urls.py
└── v2/               # Version 2 (future) ← TAMBAH INI NANTI
    ├── __init__.py
    ├── urls.py
    └── accounts/
        ├── serializers/  # Bisa beda format!
        ├── viewsets/     # Bisa beda logic!
        └── urls.py
"""

# ============================================
# 1. api/urls.py (Main routing)
# ============================================

# SEKARANG (hanya v1):
from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('v1/', include(('api.v1.urls', 'v1'), namespace='v1')),
]

# NANTI (v1 + v2):
urlpatterns = [
    path('v1/', include(('api.v1.urls', 'v1'), namespace='v1')),
    path('v2/', include(('api.v2.urls', 'v2'), namespace='v2')),  # ← ADD THIS
]


# ============================================
# 2. api/v2/urls.py (New version)
# ============================================

from django.urls import include, path

app_name = 'v2'

urlpatterns = [
    path('', include(('api.v2.accounts.urls', 'accounts'), namespace='accounts')),
]


# ============================================
# 3. api/v2/accounts/serializers/division.py
# ============================================

from rest_framework import serializers
from apps.accounts.models import Division

# V2 bisa punya format BERBEDA!
class DivisionSerializer(serializers.ModelSerializer):
    """
    V2 changes:
    - Field 'code' jadi 'division_code'
    - Field 'name' jadi 'division_name'
    - Add new field 'status'
    """
    
    division_code = serializers.CharField(source='code')
    division_name = serializers.CharField(source='name')
    status = serializers.CharField(default='active')
    
    class Meta:
        model = Division
        fields = ['id', 'division_code', 'division_name', 'status']


# ============================================
# 4. config/settings.py - Update SPECTACULAR_SETTINGS
# ============================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'Employee Management API',
    'VERSION': '1.0.0',  # Overall version
    
    # Support multiple API versions
    'SCHEMA_PATH_PREFIX': r'/api',
    
    # Servers for different versions
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Development server'},
    ],
    
    # Optional: Version in schema
    'VERSION_INFO': {
        'v1': {'description': 'Stable API version 1'},
        'v2': {'description': 'New API version 2 (beta)'},
    }
}


# ============================================
# HASIL: Swagger akan show SEMUA VERSIONS
# ============================================

"""
Swagger UI akan menampilkan:

┌─────────────────────────────────────────┐
│ Employee Management API                 │
│ Version: 1.0.0                          │
├─────────────────────────────────────────┤
│                                         │
│ 📂 V1 - Divisions                       │
│   GET    /api/v1/divisions/             │
│   POST   /api/v1/divisions/             │
│   GET    /api/v1/divisions/{id}/        │
│                                         │
│ 📂 V2 - Divisions                       │
│   GET    /api/v2/divisions/             │
│   POST   /api/v2/divisions/             │
│   GET    /api/v2/divisions/{id}/        │
│                                         │
│ Response V1:                            │
│ {                                       │
│   "id": 1,                              │
│   "code": "IT",                         │
│   "name": "IT Department"               │
│ }                                       │
│                                         │
│ Response V2:                            │
│ {                                       │
│   "id": 1,                              │
│   "division_code": "IT",                │
│   "division_name": "IT Department",     │
│   "status": "active"                    │
│ }                                       │
└─────────────────────────────────────────┘
"""


# ============================================
# BEST PRACTICES: API Versioning
# ============================================

"""
1. KAPAN BUAT V2?
   ✅ Breaking changes (field dihapus/rename)
   ✅ Major logic changes
   ✅ Perlu support old mobile apps
   
   ❌ JANGAN untuk:
   - Minor bug fixes (fix di v1)
   - Add new fields (backward compatible)
   - Internal refactoring

2. MAINTENANCE STRATEGY
   - V1: Support 1-2 tahun
   - V2: New features
   - V3: Next major version
   
   Old version bisa di-deprecate:
   - v1.0: 2024-2026 (active)
   - v2.0: 2025-2027 (active)
   - v1.0: 2027+ (deprecated, sunset)

3. DEPRECATION NOTICE
   Kasih warning di response:
   
   Response Headers:
   X-API-Version: 1.0
   X-API-Deprecated: true
   X-API-Sunset-Date: 2027-01-01
   Warning: API v1 will be deprecated on 2027-01-01

4. URL VERSIONING (Yang Anda pakai) ⭐
   ✅ /api/v1/divisions/
   ✅ /api/v2/divisions/
   
   Alternatives (TIDAK recommended):
   ❌ /api/divisions/?version=1  (Query param)
   ❌ Header: Accept: application/vnd.api.v1+json
   
   Kenapa URL versioning terbaik?
   - Clear & explicit
   - Easy to test
   - Easy to document
   - Browser-friendly

5. SHARING CODE BETWEEN VERSIONS
   # Shared model (same database)
   apps/accounts/models/division.py  ← SAMA untuk v1 & v2
   
   # Different serializers
   api/v1/accounts/serializers/division.py  ← Format v1
   api/v2/accounts/serializers/division.py  ← Format v2
   
   # Different viewsets (if needed)
   api/v1/accounts/viewsets/division.py
   api/v2/accounts/viewsets/division.py
"""


# ============================================
# TRANSITION STRATEGY
# ============================================

"""
Phase 1: V1 Only (CURRENT) ✅
├── /api/v1/divisions/
└── All clients use v1

Phase 2: V1 + V2 Beta
├── /api/v1/divisions/  (stable)
├── /api/v2/divisions/  (beta)
└── New clients try v2, old clients stay v1

Phase 3: V2 Stable, V1 Deprecated
├── /api/v1/divisions/  (deprecated, warning)
├── /api/v2/divisions/  (stable)
└── Migrate clients to v2

Phase 4: V2 Only
├── /api/v1/divisions/  (removed or redirect to v2)
└── /api/v2/divisions/  (stable)
"""


# ============================================
# KESIMPULAN
# ============================================

"""
✅ Setup Anda SEKARANG sudah BENAR!
   - OpenAPI 3.0 (modern)
   - API versioning /api/v1/ (good practice)

✅ Kapan butuh v2?
   - Nanti kalau ada breaking changes
   - Untuk sekarang v1 cukup!

✅ drf-spectacular FULL SUPPORT untuk multiple versions
   - Auto-detect semua version
   - Show semua di 1 Swagger UI
   - Clear documentation

❓ Perlu ganti sekarang?
   - TIDAK! Setup Anda sudah optimal
   - Tambah v2 nanti kalau perlu
"""
