from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, EmailOtp, Region
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


class CheckUserExistsView(GenericAPIView):
    pagination_class = None
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                "Email address",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def get(self, request):
        if email := request.GET.get("email"):
            result = {"exists": User.objects.filter(email=email).exists()}
        else:
            result = {"exists": False}
        return Response(result)


class SendOtpView(GenericAPIView):
    pagination_class = None
    serializer_class = serializers.SendOtpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.instance.send()
        return Response({"session": serializer.instance.id})


class VerifyOtpView(GenericAPIView):
    pagination_class = None
    serializer_class = serializers.VerifyOtpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.validated_data["session"]
        otp = serializer.validated_data["otp"]
        if otp_session := EmailOtp.get_verify_pendings().filter(id=session).first():
            if otp_session.otp == otp:
                otp_session.verified = True
                otp_session.save()
                return Response({"success": True})
            else:
                otp_session.attempts += 1
                otp_session.save()
            return Response({"success": False}, status=400)
        return Response(status=404)
    
    
class RegisterView(GenericAPIView):
    pagination_class = None
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        otp_session: EmailOtp = serializer.validated_data["session"]
        user.set_password(serializer.validated_data["password"])
        user.save()
        refresh = RefreshToken.for_user(user)
        otp_session.make_used()
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class ProfileView(RetrieveAPIView):
    pagination_class = None
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user



class RegionListView(ListAPIView):
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name"]
