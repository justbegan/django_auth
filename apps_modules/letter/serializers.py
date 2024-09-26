from rest_framework import serializers

from .models import Letter


class Letter_serializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()
    email = serializers.CharField(source='author.email', read_only=True)

    class Meta:
        fields = '__all__'
        model = Letter

    def get_fio(self, obj):
        return f"{obj.author.first_name} {obj.author.middle_name} {obj.author.last_name}"


class Letter_serializer_ff(serializers.Serializer):
    text = serializers.CharField()
