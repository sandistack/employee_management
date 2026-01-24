# ========================================
# SCENARIO 1: SIMPLE CRUD - CUKUP 1 SERIALIZER
# ========================================
# Cocok untuk: Model sederhana, tidak ada field computed, semua field bisa read/write

from rest_framework import serializers, viewsets
from apps.accounts.models import Position


# ✅ CUKUP 1 SERIALIZER UNTUK SEMUA!
class PositionSerializer(serializers.ModelSerializer):
    """Satu serializer untuk list, detail, create, update"""
    
    class Meta:
        model = Position
        fields = ['id', 'code', 'title', 'level', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class PositionViewSet(viewsets.ModelViewSet):
    """
    Simple ViewSet - pakai 1 serializer untuk semua action
    
    ✅ Advantages:
    - Less code
    - Easy to maintain
    - Good for simple models
    
    ❌ Trade-offs:
    - Tidak bisa customize per-action
    - Semua field selalu included
    - Bisa jadi verbose untuk list (terlalu banyak data)
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer  # ← CUKUP INI!
    
    # All actions use same serializer:
    # - list() → PositionSerializer
    # - create() → PositionSerializer
    # - retrieve() → PositionSerializer
    # - update() → PositionSerializer
    # - partial_update() → PositionSerializer


# ========================================
# HASIL API:
# ========================================

# GET /api/v1/positions/
# Response:
# {
#   "count": 100,
#   "results": [
#     {
#       "id": 1,
#       "code": "MGR",
#       "title": "Manager",
#       "level": 5,
#       "description": "Manages team...",  # ← Mungkin tidak perlu di list
#       "created_at": "2024-01-01"
#     }
#   ]
# }

# POST /api/v1/positions/
# Request:
# {
#   "code": "MGR",
#   "title": "Manager",
#   "level": 5,
#   "description": "..."
# }


# ========================================
# KAPAN PAKAI CARA INI?
# ========================================
# ✅ Model sederhana (5-10 fields)
# ✅ Tidak ada computed fields (SerializerMethodField)
# ✅ Tidak ada nested relations
# ✅ Semua field bisa read dan write
# ✅ Tidak perlu optimize performance
# ✅ Prototype/MVP phase
