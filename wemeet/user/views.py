import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Users

class AccountView(View): 

    def get(self, request): #전체 회원 조회
        userinfo = list(Users.objects.values())
        return JsonResponse({"data":userinfo},status=200)

class AccountSignUp(View):

    def post(self, request): #회원 가입
        data = json.loads(request.body)
        bytedPw = bytes(data["password"],"utf-8")
        hashPw = bcrypt.hashpw(bytedPw, bcrypt.gensalt())
        decodedPw = hashPw.decode('utf-8')
        Users.objects.create(
            name     = data["name"],
            password = decodedPw,
            email    = data["email"]
             #나머지는 null처리되며 로그인 이후 프로필설정에서 수정가능하다.

        ).save()
        return JsonResponse({"message":"SUCCESS"}, status=200)

class AccountLogin(View):

    def post(self, request): 
        data = json.loads(request.body)

        try:
            user = Users.objects.get(email=data['email'])
            encoded_jwt_id = jwt.encoded({'id':user.id},user.id,algorithm='HS256')
            if bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")})
            else :
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)
            return JsonResponse({"message":"SUCCESS"}, status=200)

        except Users.DoseNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 

        except Exception as e:
            return HttpResponse(status=500)
