from rest_framework import serializers

from users.models import CustomUser
from .models import VerificationCode


class User_serializer(serializers.ModelSerializer):
    profiles = serializers.ListField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'is_active', 'profiles', 'email',
                  'first_name', 'middle_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class User_serializer_ff(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    municipal_district_id = serializers.IntegerField(required=True)
    settlement_id = serializers.IntegerField()
    locality_id = serializers.IntegerField()
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        return validated_data


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
