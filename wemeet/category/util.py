import jwt
import json
import bcrypt
from django.http import JsonResponse,HttpResponse
from user.models import Users
from wemeet.my_settings import WEMEET_SECRET


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token_auted_user = request.headers.get('access_token', None)
            if token_auted_user:
                token_decoded_user = jwt.decode(token_auted_user, WEMEET_SECRET['secret'], algorithms = ['HS256'])
                request.user = Users.objects.get(id=token_decoded_user["id"])

                return func(self, request, *args, **kwargs)
            
            else :

                return HttpResponse({"message":"INVALID_Token"},status = 401)
        
        except Exception:

            return HttpResponse({"message":"maybe you are using IE"},status = 400)

    return wrapper