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
    path("clothes/create/", views.UserClothesCreateView.as_view(), name="user_clothes_create"),
    path("clothes/delete/<pk>/", views.UserClothesDeleteView.as_view(), name="user_clothes_delete"),
    path("clothes/types/", views.ClothesTypeListView.as_view(), name="clothes_type_list"),
    path("outfit/tags/", views.OutfitTagListView.as_view(), name="outfit_tag_list"),
    path("outfit/create/", views.UserOutfitCreateView.as_view(), name="user_outfit_create"),
    path("outfit/my/", views.UserOutfitListView.as_view(), name="user_outfit_list"),
    path("outfit/delete/<pk>/", views.UserOutfitDeleteView.as_view(), name="user_outfit_delete"),
]
