import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Users,Genders,Languages
from .util        import login_decorator
from wemeet.my_settings import WEMEET_SECRET

class AccountView(View): 
    @login_decorator
    def get(self, request):
        userinfo = list(Users.objects.values())
        return JsonResponse({"data":userinfo}, status=200)

class AccountSignUp(View):

    def post(self, request): 
        data = json.loads(request.body)
        bytedPw = bytes(data["password"],"utf-8")
        hashPw = bcrypt.hashpw(bytedPw, bcrypt.gensalt())
        decodedPw = hashPw.decode('utf-8')
        
        Users.objects.create(
            name     = data["name"],
            password = decodedPw,
            email    = data["email"],
        ).save()

        
        return JsonResponse({"message":"SUCCESS"}, status=200)

class AccountLogin(View):

    def post(self, request): 
        data = json.loads(request.body)
    
        try:
            user=Users.objects.get(email=data['email'])
            encoded_jwt_id = jwt.encode({'user_id':user.id},WEMEET_SECRET['secret'],algorithm='HS256')
            if bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")})
            else :
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)
            return JsonResponse({"message":"SUCCESS"}, status=200)

        except Users.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 

        except Exception as e:
            return HttpResponse(status=500)