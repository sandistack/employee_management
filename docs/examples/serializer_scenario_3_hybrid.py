# ========================================
# SCENARIO 3: HYBRID - 2 SERIALIZERS (RECOMMENDED!) ⭐
# ========================================
# Best of both worlds: Tidak terlalu simple, tidak terlalu complex

from rest_framework import serializers, viewsets
from apps.accounts.models import Division


# ----------------------------------------
# 1. READ SERIALIZER - Untuk GET (list & detail)
# ----------------------------------------
class DivisionReadSerializer(serializers.ModelSerializer):
    """
    Untuk GET endpoints (list + detail)
    
    💡 Ide: Gabungkan list + detail jadi 1 serializer
    - Cukup 1 serializer untuk read operations
    - Masih include computed fields
    - Masih readable & maintainable
    """
    
    employee_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = Division
        fields = [
            'id', 'code', 'name', 'description',
            'employee_count', 
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.user_set.count()


# ----------------------------------------
# 2. WRITE SERIALIZER - Untuk POST/PUT/PATCH
# ----------------------------------------
class DivisionWriteSerializer(serializers.ModelSerializer):
    """
    Untuk POST/PUT/PATCH endpoints
    
    💡 Ide: Serializer terpisah untuk input
    - No computed fields
    - No read-only fields
    - Focus on validation
    - Clean API documentation
    """
    
    class Meta:
        model = Division
        fields = ['code', 'name', 'description']
    
    def validate_code(self, value):
        value = value.upper()
        instance_id = self.instance.id if self.instance else None
        
        if Division.objects.filter(code=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError(
                f"Division dengan code '{value}' sudah ada"
            )
        
        return value


# ----------------------------------------
# 3. VIEWSET
# ----------------------------------------
class DivisionViewSet(viewsets.ModelViewSet):
    """
    ⭐ RECOMMENDED APPROACH - 2 Serializers
    
    ✅ Advantages:
    - Simple (only 2 serializers)
    - Clean input/output separation
    - Easy to maintain
    - Good documentation
    - Good performance
    
    💰 Best ROI (Return on Investment)
    """
    
    queryset = Division.objects.all()
    
    def get_serializer_class(self):
        # Read operations (GET)
        if self.action in ['list', 'retrieve']:
            return DivisionReadSerializer
        
        # Write operations (POST, PUT, PATCH)
        return DivisionWriteSerializer


# ========================================
# DECISION TREE: Berapa Serializer Yang Perlu?
# ========================================

"""
┌─────────────────────────────────────────────────────────────┐
│  Apakah model Anda SIMPLE?                                  │
│  - < 10 fields                                              │
│  - Tidak ada computed fields                                │
│  - Tidak ada relations                                      │
└─────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
       YES                     NO
        │                       │
        ↓                       ↓
  ┌──────────┐         ┌──────────────────┐
  │ 1 SERIALIZER       │  Ada computed     │
  │                    │  fields?          │
  │ ✅ Simple          │  (employee_count, │
  │ ✅ Fast            │   full_name, etc) │
  │ ✅ Easy            │                   │
  └──────────┘         └──────────────────┘
                              │
                  ┌───────────┴───────────┐
                 YES                     NO
                  │                       │
                  ↓                       ↓
          ┌──────────────┐        ┌──────────────┐
          │ 2 SERIALIZERS│        │ List return  │
          │              │        │ 50+ records? │
          │ - Read       │        │              │
          │ - Write      │        └──────────────┘
          │              │               │
          │ ⭐ RECOMMENDED│   ┌───────────┴────────┐
          └──────────────┘  YES                  NO
                             │                    │
                             ↓                    ↓
                    ┌──────────────┐      ┌──────────────┐
                    │ 3 SERIALIZERS│      │ 2 SERIALIZERS│
                    │              │      │              │
                    │ - List       │      │ - Read       │
                    │ - Detail     │      │ - Write      │
                    │ - Write      │      │              │
                    │              │      │ ⭐ RECOMMENDED│
                    │ 🚀 OPTIMIZE  │      └──────────────┘
                    └──────────────┘
"""


# ========================================
# REAL WORLD EXAMPLES
# ========================================

# 1️⃣ ONE SERIALIZER - Position (simple model)
"""
class PositionSerializer:
    fields = ['id', 'code', 'title', 'level']
    
→ Cukup 1 serializer karena:
  - Simple model
  - Tidak ada computed fields
  - Tidak ada relations
"""

# 2️⃣ TWO SERIALIZERS - Division (medium complexity)
"""
class DivisionReadSerializer:
    fields = ['id', 'name', 'employee_count', 'created_at']
    
class DivisionWriteSerializer:
    fields = ['name', 'description']
    
→ Perlu 2 serializer karena:
  - Ada computed field (employee_count)
  - Perlu pisahkan read vs write
  - Input lebih clean
"""

# 3️⃣ THREE SERIALIZERS - User/Employee (complex)
"""
class UserListSerializer:  # Lightweight
    fields = ['id', 'email', 'full_name', 'division_name']
    
class UserDetailSerializer:  # Comprehensive
    fields = [ALL FIELDS + relations + computed + metadata]
    
class UserWriteSerializer:  # Clean input
    fields = ['email', 'password', 'first_name', 'last_name']
    
→ Perlu 3 serializer karena:
  - List return 100+ users (need optimize)
  - Detail perlu show all info + relations
  - Write perlu validation khusus
  - Performance critical
"""


# ========================================
# RECOMMENDATIONS BY PROJECT PHASE
# ========================================

# 🚀 MVP / Prototype Phase
# → Use 1 serializer
# → Focus on features, not optimization
# → Refactor later if needed

# 📈 Growth Phase
# → Use 2 serializers (Read/Write)
# → Balance between simplicity & optimization
# → Most common approach

# 🏢 Enterprise / Production
# → Use 2-3 serializers as needed
# → Optimize for performance
# → Proper separation of concerns
# → Good documentation


# ========================================
# CONCLUSION
# ========================================

"""
❓ Perlu berapa serializer?

SIMPLE ANSWER:
- Start dengan 1 serializer
- Jika ada computed fields → 2 serializers (Read/Write)
- Jika performance issue → 3 serializers (List/Detail/Write)

PRACTICAL ANSWER:
- 80% cases → 2 serializers (Read/Write) ⭐
- 15% cases → 1 serializer (Simple models)
- 5% cases → 3+ serializers (Complex/optimize)

SENIOR DEVELOPER ADVICE:
"Don't over-engineer. Start simple, refactor when needed.
 2 serializers (Read/Write) adalah sweet spot untuk most cases."
"""
