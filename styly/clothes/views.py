from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, CreateAPIView
from . import serializers
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import uuid
import os
from rest_framework.response import Response
from .models import UserClothes, ClothesType, OutfitTag, UserOutfit
from rembg import remove
from PIL import Image
import io
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .service import classify_clothes


class RemoveImageBgView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = serializers.ImageUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data['image']

        input_image = uploaded_file.read()
        output_image = remove(input_image)

        output_buffer = io.BytesIO(output_image)
        processed_image = Image.open(output_buffer)

        os.makedirs("media/tmp", exist_ok=True)
        result_path = f"media/tmp/{uuid.uuid4()}.png"
        processed_image.save(result_path, format='PNG')


        classification = classify_clothes(result_path)

        clothes_type = ClothesType.objects.get_or_create(
            key=classification,
            defaults={"name": classification}
        )[0]


        return Response({
            "image_url": request.build_absolute_uri("/" + result_path),
            "type": {
                "id": clothes_type.id,
                "name": clothes_type.name,
            }
        })


class UserClothesListView(ListAPIView):
    serializer_class = serializers.UserClothesListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "type_id": ["exact"],
    }

    def get_queryset(self):
        return UserClothes.objects.filter(user=self.request.user).order_by("-id").select_related("type")


class ClothesTypeListView(ListAPIView):
    pagination_class = None
    serializer_class = serializers.ClothesTypeSerializer
    queryset = ClothesType.objects.all()



class OutfitTagListView(ListAPIView):
    pagination_class = None
    serializer_class = serializers.OutfitTagSerializer
    queryset = OutfitTag.objects.all()
    filter_backends = [filters.SearchFilter]


class UserOutfitCreateView(CreateAPIView):
    serializer_class = serializers.UserOutfitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserOutfitListView(ListAPIView):
    serializer_class = serializers.UserOutfitListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (UserOutfit.objects.filter(user=self.request.user).order_by("-id").
                prefetch_related("tags", "clothes__clothes", "clothes__clothes__type"))
