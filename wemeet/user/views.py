import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import	User, Gender, UserCategory
from category.models import Category
from .util import login_decorator
from wemeet.my_settings import WEMEET_SECRET


class AccountSignUp(View):
	def post(self, request):
		data = json.loads(request.body)

		try:
			if User.objects.filter(email = data['email']).exists():
				return JsonResponse({'messsage': 'EMAIL_EXISTS'}, status=409)

			else:
				bytedPw = bytes(data["password"], "utf-8")
				hashPw = bcrypt.hashpw(bytedPw, bcrypt.gensalt())
				decodedPw = hashPw.decode('utf-8')
				User.objects.create(
					name = data["name"],
					password = decodedPw,
					email = data["email"],
				).save()
				return JsonResponse({"message": "SUCCESS"}, status=200)

		except:
			    return JsonResponse({"message": "INVALID"}, status=400)


class AccountLogin(View):

    def post(self, request): 
        data = json.loads(request.body)
    
        try:
            user=User.objects.get(email=data['email'])
            encoded_jwt_id = jwt.encode({'user_id':user.id},WEMEET_SECRET['secret'],algorithm='HS256')

            if bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")) is False:
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)

            elif bcrypt.checkpw(data['password'].encode("UTF-8"), user.password.encode("UTF-8")):
                return JsonResponse({"access_token" : encoded_jwt_id.decode("UTF-8"),"SUCCESS":"200"}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 

class AccountDetailModify(View):

	@login_decorator
	def get(self, request):
		login_user=request.user
		result = {
            "id": login_user.id,
            "name": login_user.name,
            "email": login_user.email,
            "updated_at": login_user.updated_at,
            "profile_introduction": login_user.profile_introduction,
            "profile_photo": login_user.profile_photo,
            "gender": login_user.gender_id,
		}

		return JsonResponse({"data":result},status=200)
		
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		login_user 					    = request.user
		login_user.profile_introduction = data['profile_introduction']
		login_user.profile_photo        = data['profile_photo']
		login_user.gender               = Gender.objects.get(gender = data['gender'])
		login_user.save()		

		return JsonResponse({"message":"SUCCESS"}, status=200)

class AccountCategory(View):

	@login_decorator
	def get(self, request):
		login_user = request.user

		result = list(UserCategory.objects.select_related('category').filter(user = login_user.id).values('category'))
		return JsonResponse({"data":result,"message":"SUCCESS"}, status = 200)

	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
        
		data2 = data['category']
		length_category = len(data2)

		try:
			login_user = request.user
			cateogry_number = []
		
			for i in range(length_category):
				num = int(data2[i]["id"])
				cateogry_number.append(num)

			for j in cateogry_number:
				chosen_data = Category.objects.get(id=j)
				
				UserCategory.objects.create(
					user	 = login_user,
					category = chosen_data
				)
			return JsonResponse({"message":"SUCCESS"}, status = 200)

		except Exception as e:
			return HttpResponse(status = 500)		
