# ========================================
# SCENARIO 2: COMPLEX MODEL - PERLU MULTIPLE SERIALIZERS
# ========================================
# Cocok untuk: Model complex, ada computed fields, perlu optimize performance

from rest_framework import serializers, viewsets
from apps.accounts.models import Division


# ----------------------------------------
# 1. LIST SERIALIZER - Ringan & Cepat
# ----------------------------------------
class DivisionListSerializer(serializers.ModelSerializer):
    """
    Untuk LIST endpoint - only essential fields!
    
    ❓ Kenapa perlu serializer terpisah?
    - List biasanya return 20-100 records
    - Tidak perlu semua field (waste bandwidth)
    - Perlu computed field: employee_count
    - Performance critical!
    """
    
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Division
        fields = ['id', 'code', 'name', 'employee_count']  # ← MINIMAL!
        # NOT included: description, created_by, created_at, updated_at
    
    def get_employee_count(self, obj):
        # Ini bisa di-optimize dengan annotate
        return obj.user_set.count()


# ----------------------------------------
# 2. DETAIL SERIALIZER - Lengkap
# ----------------------------------------
class DivisionDetailSerializer(serializers.ModelSerializer):
    """
    Untuk RETRIEVE endpoint - all fields + relations!
    
    ❓ Kenapa perlu serializer terpisah?
    - Detail cuma return 1 record
    - Boleh lebih verbose
    - Include relations
    - Show metadata (created_at, updated_at, etc)
    """
    
    employee_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    employees = serializers.SerializerMethodField()  # ← Show employees
    
    class Meta:
        model = Division
        fields = [
            'id', 'code', 'name', 'description',
            'employee_count', 'employees',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.user_set.count()
    
    def get_employees(self, obj):
        # Only show first 5 employees in detail
        employees = obj.user_set.all()[:5]
        return [{'id': e.id, 'name': e.get_full_name()} for e in employees]


# ----------------------------------------
# 3. CREATE/UPDATE SERIALIZER - Input Only
# ----------------------------------------
class DivisionWriteSerializer(serializers.ModelSerializer):
    """
    Untuk CREATE & UPDATE endpoint - input fields only!
    
    ❓ Kenapa perlu serializer terpisah?
    - Tidak perlu computed fields (employee_count, etc)
    - Tidak perlu read-only fields (id, created_at, etc)
    - Focus pada validation
    - Clean request body
    """
    
    class Meta:
        model = Division
        fields = ['code', 'name', 'description']  # ← INPUT ONLY!
    
    def validate_code(self, value):
        """Custom validation untuk code"""
        value = value.upper()
        
        # Check uniqueness
        instance_id = self.instance.id if self.instance else None
        if Division.objects.filter(code=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError(
                f"Division dengan code '{value}' sudah ada"
            )
        
        return value
    
    def validate_name(self, value):
        """Name minimal 3 karakter"""
        if len(value) < 3:
            raise serializers.ValidationError("Nama minimal 3 karakter")
        return value


# ----------------------------------------
# 4. VIEWSET - Gunakan Serializer Yang Tepat
# ----------------------------------------
class DivisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet dengan multiple serializers
    
    ✅ Advantages:
    - Optimized untuk setiap use case
    - Smaller payload untuk list
    - Rich data untuk detail
    - Clean input untuk create/update
    - Better performance
    
    ❌ Trade-offs:
    - More code to maintain
    - Need to manage multiple files
    """
    
    queryset = Division.objects.all()
    
    def get_serializer_class(self):
        """Pilih serializer berdasarkan action"""
        
        if self.action == 'list':
            return DivisionListSerializer
        
        elif self.action == 'retrieve':
            return DivisionDetailSerializer
        
        elif self.action in ['create', 'update', 'partial_update']:
            return DivisionWriteSerializer
        
        # Default fallback
        return DivisionDetailSerializer


# ========================================
# PERBANDINGAN HASIL:
# ========================================

# 📋 LIST - Ringan, cepat, minimal
# GET /api/v1/divisions/
# Response:
# {
#   "results": [
#     {
#       "id": 1,
#       "code": "IT",
#       "name": "IT Department",
#       "employee_count": 25
#     }
#   ]
# }

# 📄 DETAIL - Lengkap, verbose, detailed
# GET /api/v1/divisions/1/
# Response:
# {
#   "id": 1,
#   "code": "IT",
#   "name": "IT Department",
#   "description": "Information Technology Division...",
#   "employee_count": 25,
#   "employees": [
#     {"id": 1, "name": "John Doe"},
#     {"id": 2, "name": "Jane Smith"}
#   ],
#   "created_by": 1,
#   "created_by_name": "Admin User",
#   "created_at": "2024-01-01T00:00:00Z",
#   "updated_at": "2024-01-15T10:30:00Z"
# }

# ✏️ CREATE - Clean input, no clutter
# POST /api/v1/divisions/
# Request:
# {
#   "code": "HR",
#   "name": "Human Resources",
#   "description": "HR Division"
# }


# ========================================
# KAPAN PAKAI CARA INI?
# ========================================
# ✅ Model complex (10+ fields)
# ✅ Ada computed fields (SerializerMethodField)
# ✅ Ada nested relations
# ✅ Perlu optimize bandwidth/performance
# ✅ List return banyak records
# ✅ Production-ready application
