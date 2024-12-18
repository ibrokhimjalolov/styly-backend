from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views


urlpatterns = [
    path("remove-image-bg/", views.RemoveImageBgView.as_view(), name="remove_image_bg"),
    path("clothes/my/", views.UserClothesListView.as_view(), name="user_clothes_list"),
    path("clothes/types/", views.ClothesTypeListView.as_view(), name="clothes_type_list"),
    path("outfit/tags/", views.OutfitTagListView.as_view(), name="outfit_tag_list"),
    path("outfit/create/", views.UserOutfitCreateView.as_view(), name="user_outfit_create"),
    path("outfit/my/", views.UserOutfitListView.as_view(), name="user_outfit_list"),
]
