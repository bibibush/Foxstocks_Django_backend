from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.

@method_decorator(ensure_csrf_cookie,name='dispatch')
class CSRFEnsureView(View):
    def get(self,request, *args, **kwargs):
        return JsonResponse(data={"result_message": "SUCESS","user":request.user.username if request.user else None}, safe=True, status=200)