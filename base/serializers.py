"""
To convert data from database models to JSON
"""

from django.db.models import fields
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, ProductImage, Order, Review, ShippingAddress, OrderItem


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)  # To use get_name

    # To use get__id, because in the frontend we are using _id
    _id = serializers.SerializerMethodField(read_only=True)

    # To use get_isAdmin, because in the frontend we are using isAdmin
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # Fields to return, can be ['name', 'price'] .etc.
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):  # get in get_name is not a part of field it's just a Django convention
        name = obj.first_name
        if name == "":
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
