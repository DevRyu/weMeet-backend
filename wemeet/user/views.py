import json
import jwt
import bcrypt
import datetime

from django.views import View
from django.http  import JsonResponse, HttpResponse

from wemeet.my_settings import WEMEET_SECRET
from category.models    import Category
from .util              import login_decorator
from .models            import User, Gender, UserCategory

class AccountSignUp(View):
	def post(self, request):
		data = json.loads(request.body)

		try:
			if User.objects.filter(email = data['email']).exists():
				return JsonResponse({'messsage': 'EMAIL_EXISTS'}, status=409)

            hash_password = bcrypt.hashpw(bytes(data["password"],"utf-8"), bcrypt.gensalt())

            User.objects.create(
                name     = data["name"],
                password = hash_password.decode('utf-8'),
                email    = data["email"],
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
			    return JsonResponse({"message": "INVALID_PARAMETER"}, status=400)

class AccountLogin(View):
    def post(self, request): 
        data = json.loads(request.body)
    
        try:
            user        = User.objects.get(email = data['email'])
            encoded_jwt = jwt.encode({'user_id':user.id}, WEMEET_SECRET['secret'], algorithm = 'HS256')

            if not bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)

            return JsonResponse({"access_token" : encoded_jwt.decode("UTF-8"),"SUCCESS":"200"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=404) 

class AccountInfo(View):
	@login_decorator
	def get(self, request):
		result = {
            "id"                   : request.user.id,
            "name"                 : request.user.name,
            "email"                : request.user.email,
            "updated_at"           : request.user.updated_at,
            "profile_introduction" : request.user.profile_introduction,
            "profile_photo"        : request.user.profile_photo,
            "gender"               : request.user.gender_id,
		}

		return JsonResponse({"data":result},status=200)
		
	@login_decorator
	def post(self, request):
		data                            = json.loads(request.body)
		login_user                      = request.user
		login_user.profile_introduction = data['profile_introduction']
		login_user.profile_photo        = data['profile_photo']
		login_user.gender               = Gender.objects.get(id = data['gender_id'])
		login_user.save()		

		return JsonResponse({"message":"SUCCESS"}, status=200)

class AccountCategory(View):
	@login_decorator
	def get(self, request):
		login_user = request.user
		result     = login_user.category.values()

		return JsonResponse({"data":result,"message":"SUCCESS"}, status = 200)

	@login_decorator
	def post(self, request):
		data            = json.loads(request.body)
		login_user      = request.user
		user_categories = [UserCategory(
            user = login_user,
            category = Category.objects.get(id = data["id"])
        ) for data in data["category"]]

        UserCategory.objects.bulk_create(user_categories)

        return JsonResponse({"message":"SUCCESS"}, status = 200)
