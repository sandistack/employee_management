"""
Division Serializers - Auto-generate Swagger documentation

💡 APPROACH: 2 Serializers (Read/Write) - RECOMMENDED!
   - DivisionSerializer: Untuk GET (list & detail)
   - DivisionWriteSerializer: Untuk POST/PUT/PATCH

👉 Bisa juga pakai 1 serializer saja, tapi pisah Read/Write lebih clean
"""
from rest_framework import serializers
from apps.accounts.models import Division


# ============================================
# OPTION 1: SIMPLE - 1 Serializer (Uncomment jika mau pakai ini)
# ============================================
# class DivisionSerializer(serializers.ModelSerializer):
#     """Satu serializer untuk semua - simple & easy"""
#     
#     class Meta:
#         model = Division
#         fields = ['id', 'code', 'name', 'description', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']
#     
#     def validate_code(self, value):
#         value = value.upper()
#         instance_id = self.instance.id if self.instance else None
#         if Division.objects.filter(code=value).exclude(id=instance_id).exists():
#             raise serializers.ValidationError(f"Code '{value}' sudah dipakai")
#         return value


# ============================================
# OPTION 2: RECOMMENDED - 2 Serializers (Read/Write)
# ============================================

class DivisionSerializer(serializers.ModelSerializer):
    """
    Serializer untuk READ operations (GET list & detail)
    
    Include:
    - All fields
    - Computed fields (employee_count)
    - Metadata (created_at, updated_at)
    """
    
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Division
        fields = [
            'id', 'code', 'name', 'description', 'parent', 'level',
            'employee_count',
            'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'level', 'is_active', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        """Count employee di division ini"""
        # Note: Bisa di-optimize dengan annotate di queryset
        return obj.user_set.count()


class DivisionWriteSerializer(serializers.ModelSerializer):
    """
    Serializer untuk WRITE operations (POST/PUT/PATCH)
    
    Include:
    - Only input fields
    - Validation logic
    - Clean request body
    """
    
    class Meta:
        model = Division
        fields = ['code', 'name', 'description']
    
    def validate_code(self, value):
        """Code harus uppercase dan unique"""
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
            raise serializers.ValidationError(
                "Nama division minimal 3 karakter"
            )
        return value
