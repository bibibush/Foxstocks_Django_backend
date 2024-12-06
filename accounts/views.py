from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import BaseCreateView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.form import MyUserCreationForm
from accounts.models import User
from accounts.serializers import UserSerializer


# Create your views here.

@method_decorator(ensure_csrf_cookie,name='dispatch')
class CSRFEnsureView(View):
    def get(self,request, *args, **kwargs):
        return JsonResponse(data={"result_message": "SUCCESS"}, safe=True, status=200)

class UserCreationView(BaseCreateView):
    form_class = MyUserCreationForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({"responseMessage":"회원가입이 완료되었습니다."},safe=True,status=201)

    def form_invalid(self, form):
        return JsonResponse({"errorMessage":"회원가입중 오류가 발생했습니다.","error":form.errors},safe=True,status=400)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        user_email = request.data.get("email")
        query = User.objects.get(email=user_email)
        serializer = UserSerializer(query)

        response = super().post(request,*args,**kwargs)

        return Response({**response.data,"user":serializer.data})