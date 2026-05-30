from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

class UserSerializerSignup(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'conf_password']


    def validate_username(self, value):
        user_exists = User.objects.filter(username=value).exists()
        if user_exists:
            raise serializers.ValidationError("ushbu Username bazada mavjud")
        return value


    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("parol uzunligi 8 tadan kam bolmasin")
        return value


    def validate(self, attrs):
        if attrs["password"] != attrs["conf_password"]:
            raise serializers.ValidationError("Parollar mos emas")
        return attrs


    def create(self, validated_data):
        validated_data.pop('conf_password')
        user = User.objects.create_user(**validated_data)
        return user



class UserSerializerSignin(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Login yoki Parol xato")
        attrs["user"] = user
        return attrs


class UserSerializerUpdate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def validate_username(self, value):
        current_user_id = self.context['request'].user.pk
        if User.objects.filter(username=value).exclude(pk=current_user_id).exists():
            raise serializers.ValidationError("Bu username band")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol uzunligi 8 tadan kam bolmasin")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance





