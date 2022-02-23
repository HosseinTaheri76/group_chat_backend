from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.validators import username_validator, password_validator


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[username_validator,
                    UniqueValidator(User.objects.all(), 'کاربری با این نام کاربری از قبل موجود است')
                    ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(User.objects.all(), 'کاربری با این آدرس ایمیل از قبل موجود است')]
    )
    password = serializers.CharField(max_length=128, required=True, validators=[password_validator], write_only=True)
    password2 = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate_password2(self, value):
        if self.initial_data['password'] == value:
            return value
        raise serializers.ValidationError('رمز عبور و تکرار رمز عبور مطابقت ندارند')

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
