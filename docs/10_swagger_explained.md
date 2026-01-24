# 🚀 Cara Kerja drf-spectacular (Auto-Generate Swagger)

## 🎯 Jawaban Singkat

**YA, 100% OTOMATIS!** 

Anda **TIDAK PERLU** membuat Swagger documentation secara manual. Cukup:
1. ✅ Buat Model
2. ✅ Buat Serializer  
3. ✅ Buat ViewSet/APIView
4. ✅ Daftar di urls.py
5. 🎉 **SWAGGER OTOMATIS MUNCUL!**

---

## 📊 Flow Chart: Dari Code → Swagger

```
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO PROJECT                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │  1. apps/accounts/models/division.py        │
        │     class Division(models.Model):           │
        │         name = models.CharField()           │
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │  2. api/v1/accounts/serializers/division.py │
        │     class DivisionSerializer:               │
        │         class Meta:                         │
        │             model = Division                │
        │             fields = ['id', 'name']         │
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │  3. api/v1/accounts/viewsets/division.py    │
        │     class DivisionViewSet(ModelViewSet):    │
        │         queryset = Division.objects.all()   │
        │         serializer_class = DivisionSerializer│
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │  4. api/v1/accounts/urls.py                 │
        │     router.register('divisions', ViewSet)   │
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │        drf-spectacular MAGIC! ✨             │
        │                                             │
        │  - Scan semua URL patterns                  │
        │  - Extract serializers                      │
        │  - Read docstrings                          │
        │  - Detect permissions                       │
        │  - Generate OpenAPI schema                  │
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │         SWAGGER UI AUTO-GENERATED!          │
        │                                             │
        │  ✅ GET    /api/v1/divisions/               │
        │  ✅ POST   /api/v1/divisions/               │
        │  ✅ GET    /api/v1/divisions/{id}/          │
        │  ✅ PUT    /api/v1/divisions/{id}/          │
        │  ✅ PATCH  /api/v1/divisions/{id}/          │
        │  ✅ DELETE /api/v1/divisions/{id}/          │
        │                                             │
        │  + Request/Response examples                │
        │  + Authentication info                      │
        │  + Try it out feature                       │
        └─────────────────────────────────────────────┘
```

---

## 🔍 Apa yang Di-detect OTOMATIS?

### 1. **URL Patterns** ← Dari urls.py
```python
# urls.py
router.register(r'divisions', DivisionViewSet)

# ✅ Otomatis detect:
# - Base URL: /api/v1/divisions/
# - Detail URL: /api/v1/divisions/{id}/
# - Custom actions: /api/v1/divisions/{id}/statistics/
```

### 2. **HTTP Methods** ← Dari ViewSet type
```python
class DivisionViewSet(viewsets.ModelViewSet):
    # ✅ Otomatis generate:
    # - list()    → GET    /divisions/
    # - create()  → POST   /divisions/
    # - retrieve()→ GET    /divisions/{id}/
    # - update()  → PUT    /divisions/{id}/
    # - partial_update() → PATCH /divisions/{id}/
    # - destroy() → DELETE /divisions/{id}/
```

### 3. **Request/Response Format** ← Dari Serializer
```python
class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name', 'code']

# ✅ Swagger auto show:
# Request body example:
# {
#   "name": "IT Department",
#   "code": "IT"
# }
#
# Response example:
# {
#   "id": 1,
#   "name": "IT Department",
#   "code": "IT"
# }
```

### 4. **Authentication** ← Dari permission_classes
```python
class DivisionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

# ✅ Swagger auto show:
# - 🔒 Lock icon di Swagger
# - Butuh Bearer token
# - Response 401 jika tidak authenticated
```

### 5. **Filters & Search** ← Dari filter_backends
```python
class DivisionViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']

# ✅ Swagger auto show query parameters:
# - ?search=IT
# - ?ordering=name
# - ?ordering=-created_at
```

### 6. **Pagination** ← Dari REST_FRAMEWORK settings
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ✅ Swagger auto show:
# - ?page=1
# - ?page=2
# Response format:
# {
#   "count": 100,
#   "next": "http://...?page=2",
#   "previous": null,
#   "results": [...]
# }
```

---

## 🎨 Level Documentation

### Level 1: ZERO Config (Basic Auto-detection)

```python
# Cukup ini saja:
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
```

**Result:** Swagger muncul dengan info minimal (URL, methods, fields)

---

### Level 2: With Docstrings (Better)

```python
class DivisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk manage divisions.
    
    - List all divisions
    - Create new division
    - Update/delete division
    """
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
```

**Result:** Swagger muncul dengan description dari docstring

---

### Level 3: With @extend_schema (Professional) ⭐

```python
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary='List all divisions',
        description='Get paginated list with search & filter',
        tags=['Divisions'],
    ),
    create=extend_schema(
        summary='Create division',
        tags=['Divisions'],
    ),
)
class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
```

**Result:** Swagger dengan:
- ✅ Custom summaries
- ✅ Detailed descriptions  
- ✅ Grouped by tags
- ✅ Custom responses
- ✅ Examples

---

## 📝 Tutorial: Menambah API Baru (Step-by-Step)

### Skenario: Buat API untuk **Position**

#### Step 1: Buat Serializer

```bash
# Buat file baru
touch api/v1/accounts/serializers/position.py
```

```python
# api/v1/accounts/serializers/position.py
from rest_framework import serializers
from apps.accounts.models import Position

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'code', 'title', 'level', 'description']
```

#### Step 2: Buat ViewSet

```bash
# Buat file baru
touch api/v1/accounts/viewsets/position.py
```

```python
# api/v1/accounts/viewsets/position.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.accounts.models import Position
from api.v1.accounts.serializers.position import PositionSerializer

class PositionViewSet(viewsets.ModelViewSet):
    """API untuk manage positions"""
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
```

#### Step 3: Daftar di URLs

```python
# api/v1/accounts/urls.py
from api.v1.accounts.viewsets.position import PositionViewSet

router = DefaultRouter()
router.register(r'divisions', DivisionViewSet, basename='division')
router.register(r'positions', PositionViewSet, basename='position')  # ← ADD THIS!
```

#### Step 4: Refresh Browser

```
http://localhost:8000/api/docs/
```

**🎉 DONE! Position API langsung muncul di Swagger!**

Akan ada:
- GET /api/v1/positions/
- POST /api/v1/positions/
- GET /api/v1/positions/{id}/
- PUT /api/v1/positions/{id}/
- PATCH /api/v1/positions/{id}/
- DELETE /api/v1/positions/{id}/

**Tidak perlu konfigurasi Swagger sama sekali!**

---

## 🔧 Advanced: Custom Actions

### Contoh: Endpoint Custom

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class DivisionViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get division statistics"""
        division = self.get_object()
        return Response({
            'employee_count': division.user_set.count(),
            'active_count': division.user_set.filter(is_active=True).count(),
        })
```

**Result:** Otomatis muncul endpoint baru di Swagger:
```
GET /api/v1/divisions/{id}/statistics/
```

---

## 🎯 Summary

### Yang OTOMATIS:
✅ URL detection  
✅ HTTP methods  
✅ Request/Response format  
✅ Authentication requirements  
✅ Query parameters (filters, search, pagination)  
✅ Field validation  
✅ Error responses  

### Yang OPTIONAL (untuk improve documentation):
📝 `@extend_schema` decorator  
📝 Docstrings  
📝 Custom examples  
📝 Custom descriptions  

### Yang TIDAK PERLU:
❌ Manual Swagger configuration  
❌ Manual endpoint listing  
❌ Manual request/response examples  
❌ Manual authentication setup  

---

## 🚀 Quick Reference

### Buat API Baru = 3 Steps:

1. **Serializer** → Define data format
2. **ViewSet** → Define logic
3. **urls.py** → Register to router

**That's it!** Swagger otomatis update! 🎉

### Cek Hasil:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema: http://localhost:8000/api/schema/

---

## 💡 Pro Tips

### 1. Use Different Serializers for Different Actions
```python
def get_serializer_class(self):
    if self.action == 'list':
        return DivisionListSerializer  # Ringan
    elif self.action in ['create', 'update']:
        return DivisionCreateSerializer  # Untuk input
    return DivisionDetailSerializer  # Lengkap
```

### 2. Group API by Tags
```python
@extend_schema(tags=['Divisions'])  # Group bersama
class DivisionViewSet(...):
    pass

@extend_schema(tags=['Divisions'])  # Same tag
class DivisionSimpleView(...):
    pass
```

### 3. Add Examples
```python
from drf_spectacular.utils import OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'IT Department',
            value={'name': 'IT', 'code': 'IT'},
            request_only=True,
        ),
    ]
)
```

### 4. Validate Schema
```bash
# Check if schema valid
python manage.py spectacular --validate

# Generate schema file
python manage.py spectacular --file schema.yml
```

---

## 🐛 Common Issues

### Q: API baru tidak muncul di Swagger?
**A:** Hard refresh browser (Ctrl+Shift+R) atau clear cache

### Q: Request format salah di Swagger?
**A:** Check serializer class yang dipakai di `get_serializer_class()`

### Q: Authentication tidak work di Swagger?
**A:** Click "Authorize" button, masukkan `Bearer <your-token>`

### Q: Want to hide endpoint from documentation?
```python
@extend_schema(exclude=True)
class InternalAPIView(...):
    pass
```

---

## 🎓 Next Steps

1. ✅ Jalankan server: `python manage.py runserver`
2. ✅ Buka: http://localhost:8000/api/docs/
3. ✅ Lihat API Division yang baru saya tambahkan
4. ✅ Try testing register → login → get divisions
5. ✅ Buat API Position dengan cara yang sama
6. ✅ Explore custom actions (@action decorator)

**Selamat! Anda sekarang paham cara kerja auto-generate API documentation!** 🎉
