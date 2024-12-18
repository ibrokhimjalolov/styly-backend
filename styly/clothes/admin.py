from django.contrib import admin
from .models import ClothesType, UserClothes, OutfitClothes, OutfitTag, UserOutfit


admin.site.register(ClothesType)
admin.site.register(UserClothes)
admin.site.register(OutfitClothes)
admin.site.register(OutfitTag)
admin.site.register(UserOutfit)

