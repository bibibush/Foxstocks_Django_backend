from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.

@method_decorator(ensure_csrf_cookie,name='dispatch')
class CSRFEnsureView(View):
    def get(self,request, *args, **kwargs):
        return JsonResponse(data={"result_message": "SUCESS"}, safe=True, status=200)