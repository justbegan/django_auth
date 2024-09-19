from rest_framework import serializers

from .models import Question


class Question_serializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class Question_serializer_ff(serializers.Serializer):
    # ff - for frontend
    question = serializers.CharField()
    answer = serializers.CharField()
