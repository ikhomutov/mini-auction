from rest_framework import serializers

from auction.core import models


class PetDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pet
        fields = ('id', 'name', 'breed')


class LotDisplaySerializer(serializers.ModelSerializer):
    pet = PetDisplaySerializer(read_only=True)
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
