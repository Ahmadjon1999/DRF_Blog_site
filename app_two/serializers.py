from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Post, Comment, Like

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    conf_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = User
        fields = ["first_name", "last_name", "username", "password", "conf_password"]

    def validate_username(self, value):
        user_exists = User.objects.filter(username=value).exists()
        if user_exists:
            raise serializers.ValidationError("Ushbu username band")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol uzunlig 8 ta belgidan kam")
        if not value.isalnum():
            raise serializers.ValidationError("Parolda faqat son va xarflar qatnashsin")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["conf_password"]:
            raise serializers.ValidationError("parollar mos emas")
        return attrs

    def create(self, validated_data):
        validated_data.pop("conf_password")
        user = User.objects.create_user(**validated_data)

        return user



class SigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(username=username, password=password)
        if user:
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("Login yoki Parol xato")


class Profil_detail_serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]



class UserSerializerUpdate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]

    def validate_username(self, value):
        current_user_id = self.context["request"].user.pk
        if User.objects.filter(username=value).exclude(pk=current_user_id).exists():
            raise serializers.ValidationError("Bu username band")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol uzunligi 8 tadan kam bolmasin")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        super().update(instance, validated_data)
        instance.save()
        return instance


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']




class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "image", "author", "category",
                  "likes_count", "comments_count", "create_at", "update_at"]

        read_only_fields = ["author", "create_at", "update_at"]



class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "create_at", "user"]





