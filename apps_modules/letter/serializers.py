from rest_framework import serializers

from .models import Letter
from apps.profiles.models import Profile


class Letter_serializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Letter

    def get_fio(self, obj):
        profile = Profile.objects.get(user=obj.author)
        return profile.fio

    def get_email(self, obj):
        profile = Profile.objects.get(user=obj.author)
        return profile.email


class Letter_serializer_ff(serializers.Serializer):
    text = serializers.CharField()
