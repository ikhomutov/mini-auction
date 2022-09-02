from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from auction.core import models


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        models.UserAccount.objects.create(
            user=user, balance=settings.DEFAULT_USER_BALANCE
        )

        return user


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pet
        fields = ('id', 'name', 'breed')
        read_only_fields = ['id']


class LotDisplaySerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Lot
        fields = ('id', 'pet', 'price', 'author')


class LotCreateSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=models.Pet.objects.all())

    class Meta:
        model = models.Lot
        fields = ('pet', 'price')


class BidShortDisplaySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Bid
        fields = ('id', 'price', 'author')


class BidLongDisplaySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    lot = LotDisplaySerializer()

    class Meta:
        model = models.Bid
        fields = ('id', 'price', 'author', 'lot',)


class BidCreateSerializer(serializers.ModelSerializer):
    lot = serializers.PrimaryKeyRelatedField(queryset=models.Lot.objects.all())

    class Meta:
        model = models.Bid
        fields = ('price', 'lot')
