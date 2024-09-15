from rest_framework import serializers
from .models import EmailOtp, User, Region
from uuid import uuid4


class SendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOtp
        fields = ["email"]
        extra_kwargs = {
            "email": {"required": True}
        }


class VerifyOtpSerializer(serializers.ModelSerializer):
    session = serializers.UUIDField()
    
    class Meta:
        model = EmailOtp
        fields = ["session", "otp"]
        extra_kwargs = {
            "session": {"required": True},
            "otp": {"required": True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    session = serializers.PrimaryKeyRelatedField(queryset=EmailOtp.objects.all(), write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "full_name", "password", "session"]
        extra_kwargs = {
            "email": {"required": True},
            "full_name": {"required": True}
        }

    def validate_session(self, value):
        if not value or not value.is_verified():
            raise serializers.ValidationError("Invalid OTP")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["email"] != attrs["session"].email:
            raise serializers.ValidationError("Email mismatch")
        return attrs

    def save(self, **kwargs):
        user = User.objects.create_user(
            email=self.validated_data["email"],
            full_name=self.validated_data["full_name"],
            username=str(uuid4())
        )
        self.instance = user
        return self.instance


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]
        

class UserProfileSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "birth_date", "gender", "region"]
