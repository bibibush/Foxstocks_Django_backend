from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import CSRFEnsureView, CustomTokenObtainPairView

app_name = "accounts"

urlpatterns = [
    path("",CSRFEnsureView.as_view()),
    path("token/",CustomTokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view())
]