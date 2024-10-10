from rest_framework import serializers

from users.models import CustomUser
from .models import VerificationCode


class User_serializer(serializers.ModelSerializer):
    profiles = serializers.ListField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'is_active', 'profiles', 'email',
                  'first_name', 'middle_name', 'last_name', 'current_section']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class User_put_serializer(serializers.ModelSerializer):
    profiles = serializers.ListField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_active', 'profiles', 'email',
                  'first_name', 'middle_name', 'last_name', 'current_section']


class User_serializer_ff(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        return validated_data

    def update(self, validated_data):
        return validated_data


class User_post_serializer_ff(User_serializer_ff):
    password = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            VerificationCode.objects.get(user=user, code=code)
        except (CustomUser.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError("Неверный код или email.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
        VerificationCode.objects.filter(user=user).delete()


class Repeat_email_ff(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return validated_data


class Recover_password_ff(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return validated_data
