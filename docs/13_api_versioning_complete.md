# 🚀 API Versioning Setup - Complete Guide

## ✅ Current Setup (v1)

Your API is now properly configured with versioning support!

### Structure:
```
/api/v1/divisions/          ← Version 1
/api/v1/positions/          ← Version 1
/api/v1/login/              ← Version 1
```

### Swagger UI:
- All endpoints show full path: `/api/v1/...`
- Base URL set to include v1
- Ready for future versions!

---

## 🎯 Benefits of Your Current Setup

### 1. **Clear Versioning**
```python
SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api/v1',  # ← Explicit v1
    'SERVERS': [
        {'url': 'http://localhost:8000/api/v1', ...}  # ← v1 in base URL
    ],
}
```

### 2. **Better Documentation**
- Description includes versioning info
- Instructions for authentication
- Grouped by tags (Authentication, Users, Divisions, etc)

### 3. **Production Ready**
```python
'SERVERS': [
    {'url': 'http://localhost:8000/api/v1', ...},     # Dev
    # {'url': 'https://api.company.com/api/v1', ...}, # Prod (uncomment later)
],
```

---

## 📋 How to Add v2 (Future)

### Step 1: Create v2 Structure

```bash
# Create v2 folder structure
mkdir -p api/v2
mkdir -p api/v2/accounts/{serializers,viewsets}
touch api/v2/__init__.py
touch api/v2/urls.py
touch api/v2/accounts/{__init__.py,urls.py}
```

### Step 2: Create v2 URLs

```python
# api/v2/urls.py
from django.urls import include, path

app_name = 'v2'

urlpatterns = [
    path('', include(('api.v2.accounts.urls', 'accounts'), namespace='accounts')),
]
```

### Step 3: Register v2 in Main API URLs

```python
# api/urls.py
from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('v1/', include(('api.v1.urls', 'v1'), namespace='v1')),
    path('v2/', include(('api.v2.urls', 'v2'), namespace='v2')),  # ← ADD THIS
]
```

### Step 4: Create v2 Serializers & ViewSets

```python
# api/v2/accounts/serializers/division.py
from rest_framework import serializers
from apps.accounts.models import Division

class DivisionSerializer(serializers.ModelSerializer):
    """
    V2 changes:
    - Renamed 'code' to 'division_code'
    - Added 'status' field
    - Different response format
    """
    
    division_code = serializers.CharField(source='code')
    status = serializers.CharField(default='active')
    
    class Meta:
        model = Division
        fields = ['id', 'division_code', 'name', 'status']


# api/v2/accounts/viewsets/division.py
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema
from api.v2.accounts.serializers.division import DivisionSerializer

@extend_schema_view(
    list=extend_schema(tags=['Divisions V2']),
    retrieve=extend_schema(tags=['Divisions V2']),
)
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
```

### Step 5: Update Spectacular Settings (Optional)

```python
# config/settings.py

# If you want separate schemas for v1 and v2:
SPECTACULAR_SETTINGS = {
    ...
    'SERVERS': [
        {'url': 'http://localhost:8000/api/v1', 'description': 'API v1'},
        {'url': 'http://localhost:8000/api/v2', 'description': 'API v2 (Beta)'},
    ],
    
    'TAGS': [
        {'name': 'Authentication', 'description': '...'},
        {'name': 'Divisions', 'description': 'v1 Division endpoints'},
        {'name': 'Divisions V2', 'description': 'v2 Division endpoints (New format)'},
    ],
}
```

---

## 🎨 Multiple Schema Strategy (Advanced)

### Option A: Single Schema (All Versions Together)

**Current setup** - Simplest approach ✅

```
GET /api/schema/           ← All versions in one schema
GET /api/docs/             ← Swagger shows all versions
```

**Pros:**
- ✅ Easy to maintain
- ✅ See all versions at once
- ✅ Good for small APIs

**Cons:**
- ❌ Can be cluttered with many versions

---

### Option B: Separate Schemas Per Version

**Advanced** - For large APIs with many versions

```python
# config/urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # V1 Schema
    path('api/v1/schema/', SpectacularAPIView.as_view(
        urlconf='api.v1.urls'
    ), name='schema-v1'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(
        url_name='schema-v1'
    ), name='swagger-ui-v1'),
    
    # V2 Schema
    path('api/v2/schema/', SpectacularAPIView.as_view(
        urlconf='api.v2.urls'
    ), name='schema-v2'),
    path('api/v2/docs/', SpectacularSwaggerView.as_view(
        url_name='schema-v2'
    ), name='swagger-ui-v2'),
]
```

**Result:**
```
GET /api/v1/docs/          ← Swagger for v1 only
GET /api/v2/docs/          ← Swagger for v2 only
```

**Pros:**
- ✅ Clean separation
- ✅ Each version has its own docs
- ✅ Good for complex APIs

**Cons:**
- ❌ More setup
- ❌ Duplicate some config

---

## 📊 Version Comparison Example

### V1 Response:
```json
GET /api/v1/divisions/1/

{
  "id": 1,
  "code": "IT",
  "name": "IT Department",
  "description": "...",
  "employee_count": 25,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### V2 Response (Different Format):
```json
GET /api/v2/divisions/1/

{
  "id": 1,
  "division_code": "IT",
  "division_name": "IT Department",
  "status": "active",
  "metadata": {
    "employee_count": 25,
    "created": "2024-01-01"
  }
}
```

---

## 🔄 Migration Strategy

### Phase 1: V1 Only (Current) ✅
```
Status: Stable
Support: Full
Clients: All use v1
```

### Phase 2: V1 + V2 Beta
```
Status: 
  - v1: Stable (maintenance mode)
  - v2: Beta (new features)
  
Support:
  - v1: Bug fixes only
  - v2: Active development
  
Clients:
  - Old: Stay on v1
  - New: Use v2
  
Duration: 3-6 months
```

### Phase 3: V2 Stable, V1 Deprecated
```
Status:
  - v1: Deprecated (sunset notice)
  - v2: Stable
  
Response Headers (v1):
  X-API-Deprecated: true
  X-API-Sunset-Date: 2026-12-31
  Warning: "API v1 will be removed on 2026-12-31"
  
Clients: Migrate from v1 to v2

Duration: 6-12 months
```

### Phase 4: V2 Only
```
Status:
  - v1: Removed or redirects to v2
  - v2: Stable
  
Support: v2 only
```

---

## 🛡️ Backward Compatibility

### Do's ✅
- Add new fields
- Add new endpoints
- Add optional parameters
- Deprecate (don't remove) fields
- Add new values to enums

### Don'ts ❌
- Remove fields
- Rename fields
- Change field types
- Remove endpoints
- Change response structure
- Make optional params required

**If you need to break compatibility → Create v2!**

---

## 📝 Deprecation Notice Implementation

### In Response (v1):
```python
from rest_framework.response import Response

class DivisionViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add deprecation headers
        response['X-API-Version'] = '1.0'
        response['X-API-Deprecated'] = 'true'
        response['X-API-Sunset-Date'] = '2026-12-31'
        response['Link'] = '</api/v2/divisions/>; rel="alternate"'
        
        return response
```

### In Documentation:
```python
@extend_schema(
    deprecated=True,  # Show deprecated badge in Swagger
    description='''
    ⚠️ DEPRECATED: This endpoint will be removed on 2026-12-31
    
    Please migrate to v2: /api/v2/divisions/
    
    Changes in v2:
    - Field 'code' renamed to 'division_code'
    - New field 'status' added
    - Better performance
    ''',
)
class DivisionViewSet(viewsets.ModelViewSet):
    pass
```

---

## 🎯 Best Practices Summary

### 1. **Start Simple**
- Begin with v1
- Add v2 only when needed
- Don't over-engineer

### 2. **Communication**
- Document breaking changes
- Give advance notice (6-12 months)
- Provide migration guide

### 3. **Versioning Strategy**
- URL versioning (what you use) ✅
- Semantic versioning (1.0, 2.0, 3.0)
- Clear deprecation policy

### 4. **Testing**
- Test both versions
- Automated API tests
- Monitor usage metrics

### 5. **Monitoring**
```python
# Track version usage
import logging

logger = logging.getLogger(__name__)

class VersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/api/'):
            version = 'v2' if '/v2/' in request.path else 'v1'
            logger.info(f"API {version} accessed: {request.path}")
        
        return self.get_response(request)
```

---

## 🚀 Current Setup Summary

Your configuration now includes:

✅ **Clear versioning** in URLs (`/api/v1/`)  
✅ **Proper OpenAPI 3.0** documentation  
✅ **Detailed descriptions** with versioning info  
✅ **Grouped endpoints** by tags  
✅ **Authentication instructions**  
✅ **Multiple server support** (dev/prod)  
✅ **Ready for v2** when needed  

**No changes needed now! Add v2 only when you have breaking changes.** 🎉

---

## 📚 Resources

- [API Versioning Best Practices](https://restfulapi.net/versioning/)
- [drf-spectacular Versioning](https://drf-spectacular.readthedocs.io/en/latest/customization.html)
- [Semantic Versioning](https://semver.org/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
