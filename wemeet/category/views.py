import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Categories
from group.models import Groups
from .util        import login_decorator
from wemeet.my_settings import WEMEET_SECRET


class CategoriesList(View):

    def get(self, request):
        category_info = list(Categories.objects.values())
        return JsonResponse({"data":category_info,"message":"SUCCESS"},status=200)


