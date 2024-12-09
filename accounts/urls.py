from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from accounts.views import CSRFEnsureView, CustomTokenObtainPairView, UserCreationView, MyProfileAPIView

app_name = "accounts"

urlpatterns = [
    path("",CSRFEnsureView.as_view()),
    path("token/",CustomTokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("create/",UserCreationView.as_view()),
    path("my-profile/<int:pk>/",MyProfileAPIView.as_view())
]