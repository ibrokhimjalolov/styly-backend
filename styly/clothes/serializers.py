from rest_framework import serializers
from .models import UserClothes, ClothesType, OutfitTag, UserOutfit, OutfitClothes


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ClothesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesType
        fields = (
            "id",
            "name",
        )


class UserClothesListSerializer(serializers.ModelSerializer):
    type = ClothesTypeSerializer()

    class Meta:
        model = UserClothes
        fields = (
            "id",
            "name",
            "image",
            "type",
            "created_at",
        )


class OutfitTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfitTag
        fields = (
            "id",
            "name",
        )


class OutfitClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutfitClothes
        fields = (
            "clothes",
            "pos_x",
            "pos_y",
            "pos_z",
        )


class UserOutfitCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=OutfitTag.objects.all(), many=True)
    clothes = OutfitClothesSerializer(many=True, write_only=True)

    class Meta:
        model = UserOutfit
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "clothes",
        )

    def create(self, validated_data):
        clothes_data = validated_data.pop("clothes")
        tags = validated_data.pop("tags")
        outfit = UserOutfit.objects.create(**validated_data)
        for tag in tags:
            outfit.tags.add(tag)
        for clothes in clothes_data:
            OutfitClothes.objects.create(outfit=outfit, **clothes)
        return outfit


class OutfitClothesReadSerializer(serializers.ModelSerializer):
    clothes = UserClothesListSerializer()

    class Meta:
        model = OutfitClothes
        fields = (
            "clothes",
            "pos_x",
            "pos_y",
            "pos_z",
        )


class UserOutfitListSerializer(serializers.ModelSerializer):
    tags = OutfitTagSerializer(many=True)
    clothes = OutfitClothesReadSerializer(many=True)

    class Meta:
        model = UserOutfit
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "clothes",
            "created_at",
        )
