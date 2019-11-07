import json
import jwt
import bcrypt
import datetime
from django.views import View
from django.http  import JsonResponse,HttpResponse
from .models      import Group, GroupCategory
from category.models import Category
from user.models  import User
from .util        import login_decorator
from wemeet.my_settings import WEMEET_SECRET


class GroupMake(View):  
    
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        new_group = Group.objects.create(
            name         = data["name"],
            introduction = data["introduction"],
            mainphoto    = data["mainphoto"],
            host         = user
        )
            
        return JsonResponse({"group_id":new_group.id,"message":"SUCCESS"}, status = 200)

class GroupAllList(View):

    @login_decorator
    def get(self, request):

        user = list(Group.objects.filter(host = request.user.id).values())
        return JsonResponse({"message":user}, status=200)

class GroupCategoryList(View):

    def get(self, request, pk):

        result = list(GroupCategory.objects.select_related('category').filter(group = pk).values('category'))
        return JsonResponse({"data":result,"message":"SUCCESS"}, status=200)

    @login_decorator
    def post(self, request, pk):
        
        data = json.loads(request.body)
        data2 = data['category']
        length_category = len(data2)
        chosen_group = Group.objects.get(id=pk)

        try:
            login_user = request.user
            cateogry_number=[]
		
            for i in range(length_category):
                num = int(data2[i]["id"])
                cateogry_number.append(num)
        
            for j in cateogry_number:
                chosen_data = Category.objects.get(id=j)

                GroupCategory.objects.create(
                    group	 = chosen_group,
                    category = chosen_data
	            )
            return JsonResponse({"message":"SUCCESS"}, status = 200)
                
        except Exception as e:
            print(e)
            return HttpResponse(status = 500)


class GroupDetailView(View):
    
    @login_decorator
    def get(self, request, pk):

        host_user_id = request.user.id
        page_now = Group.objects.get(id = pk)

        if page_now.host.id == host_user_id:
            page_detail = list(Group.objects.filter(id = pk).values())
            return JsonResponse({"data":page_detail,"who":"host","message":"SUCCESS"}, status = 200)
            
        else :
            page_detail = list(Group.objects.filter(id = pk).values())            
            return JsonResponse({"data":page_detail,"who":"user","message":"SUCCESS"}, status = 200)