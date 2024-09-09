from rest_framework import serializers

from .models import Question, Answer


class Question_serializer(serializers.ModelSerializer):
    get_answer = serializers.DictField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'author': {'write_only': True}
        }


class Answer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            'author': {'write_only': True}
        }
