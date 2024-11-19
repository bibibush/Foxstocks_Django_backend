from django.urls import path

from accounts.views import CSRFEnsureView

app_name = "accounts"

urlpatterns = [
    path("",CSRFEnsureView.as_view())
]