import json
import jwt
import bcrypt
import datetime

from django.views import View
from django.http  import JsonResponse,HttpResponse

from .models      import Category
from group.models import Group
from .util        import login_decorator
from wemeet.my_settings import WEMEET_SECRET

class CategoriesList(View):
    def get(self, request):
        return JsonResponse({"data": Category.objects.values()},status = 200)


