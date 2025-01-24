from django.db import models

from users.models import User


class ClothesType(models.Model):
    name = models.CharField(max_length=255)
    key = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clothes_type"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.name)


class UserClothes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="clothes-images/%Y/%m/%d")

    type = models.ForeignKey(ClothesType, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_clothes"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.name)


class OutfitTag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_clothes_tag"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.name)


class UserOutfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()

    tags = models.ManyToManyField(OutfitTag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_outfit"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.name)


class OutfitClothes(models.Model):
    outfit = models.ForeignKey(UserOutfit, on_delete=models.CASCADE, related_name="clothes")
    clothes = models.ForeignKey(UserClothes, on_delete=models.CASCADE)

    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    pos_z = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "outfit_clothes"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.outfit} - {self.clothes}"
