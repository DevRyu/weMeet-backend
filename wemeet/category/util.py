import jwt
import json
import bcrypt
from django.http import JsonResponse,HttpResponse
from user.models import User
from wemeet.my_settings import WEMEET_SECRET

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs): 
   
        if "Authorization" not in request.headers: 
            return JsonResponse({"error_code":"INVALID_LOGIN"}, status = 401)
        
        encode_token = request.headers["Authorization"] 

        try:
            data = jwt.decode(encode_token, WEMEET_SECRET['secret'], algorithm = 'HS256') 
            user = User.objects.get(id = data["user_id"])
            request.user = user 

        except jwt.DecodeError: 
            return JsonResponse({
                "error_code" : "INVALID_TOKEN"
            }, status = 401) 

        except User.DoesNotExist:
            return JsonResponse({
                "error_code" : "UNKNOWN_USER"
            }, status = 401) 

        return func(self, request, *args, **kwargs) 

    return wrapper
