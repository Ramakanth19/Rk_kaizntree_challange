from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item, Category

class LoginSerializer(serializers.Serializer):
    # Fields for username and password for login
    username = serializers.CharField()
    password = serializers.CharField()

    # Custom validation method to authenticate the user
    def validate(self, data):
        # Uses Django's authenticate method to verify credentials
        user = authenticate(**data)
        if user and user.is_active:
            # If authentication is successful and user is active, return user object
            return user
        # Raise validation error if authentication fails
        raise serializers.ValidationError("Incorrect Credentials")

class registerSerializer(serializers.ModelSerializer):
    # Serializer for registering a new user with username, password, and email
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only for security

    def create(self, validated_data):
        # Create a new user instance with the validated data
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    # Serializer for Category model, includes all fields in the model
    class Meta:
        model = Category
        fields = '__all__'# Serialize all fields from the Category model

class ItemSerializer(serializers.ModelSerializer):
    # Custom field to display the category name using a method field
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__' # Serialize all fields from the Item model
        
    def get_category_name(self, obj):
        # Method to get the name of the category related to an item
        return obj.category.name
