import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Users, Genders, Languages
from .util import login_decorator
from wemeet.my_settings import WEMEET_SECRET


class AccountSignUp(View):
	def post(self, request):
		data = json.loads(request.body)
		try:
			if Users.objects.filter(email=data['email']).exists():
				return JsonResponse({'messsage': 'EMAIL_EXISTS'}, status=409)

			else:
				bytedPw = bytes(data["password"], "utf-8")
				hashPw = bcrypt.hashpw(bytedPw, bcrypt.gensalt())
				decodedPw = hashPw.decode('utf-8')
				Users.objects.create(
					name=data["name"],
					password=decodedPw,
					email=data["email"],
				).save()
				return JsonResponse({"message": "SUCCESS"}, status=200)
		except:
			    return JsonResponse({"message": "INVALID"}, status=400)



# class AccountSignUpDetal(View):

class AccountLogin(View):

    def post(self, request): 
        data = json.loads(request.body)
    
        try:
            user=Users.objects.get(email=data['email'])
            encoded_jwt_id = jwt.encode({'user_id':user.id},WEMEET_SECRET['secret'],algorithm='HS256')

            if bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")) is False:
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)
            elif bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8")}, status=200)

        except Users.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 
