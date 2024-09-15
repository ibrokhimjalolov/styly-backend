from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path("opt/send/", views.SendOtpView.as_view(), name="send_otp"),
    path("opt/verify/", views.VerifyOtpView.as_view(), name="verify_otp"),
    
    path('users/check-user-exists/', views.CheckUserExistsView.as_view(), name='check_user_exists'),
    path('users/register/', views.RegisterView.as_view(), name='register'),
    path("users/profile/", views.ProfileView.as_view(), name="profile"),
    
    path("common/regions/", views.RegionListView.as_view(), name="region_list"),
]
