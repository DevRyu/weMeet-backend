import json
import jwt
import bcrypt
import datetime

from django.views import View
from django.http  import JsonResponse,HttpResponse

from .models            import Group, GroupCategory
from category.models    import Category
from user.models        import User
from .util              import login_decorator
from wemeet.my_settings import WEMEET_SECRET


class GroupView(View):  
    @login_decorator
    def post(self,request):
        try:
            data      = json.loads(request.body)
            new_group = Group.objects.create(
                name         = data["name"],
                introduction = data["introduction"],
                mainphoto    = data["mainphoto"],
                host         = user
            )
                
            return JsonResponse({"group_id":new_group.id,"message":"SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({"error": "INVALID_KEY"}, status = 400)

class GroupListView(View):
    @login_decorator
    def get(self, request):
        return JsonResponse({"message" : request.user.groups.values()}, status=200)

class GroupCategoryList(View):
    def get(self, request, category_id):
        result = list(GroupCategory.objects.select_related('category').filter(group = category_id).values('category'))

        return JsonResponse({"data":result,"message":"SUCCESS"}, status=200)

    @login_decorator
    def post(self, request, pk):
        ## 위에 변경 사항과 동일하니 참조 하세요
        data            = json.loads(request.body)
        data2           = data['category']
        length_category = len(data2)
        chosen_group    = Group.objects.get(id     = pk)

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
            return HttpResponse(status = 500)

class GroupDetailView(View):
    @login_decorator
    def get(self, request, group_id):
        groups = Group.objects.filter(id = group_id).values()

        return JsonResponse({
            "data" : list(group),
            "host" : group.host.id == request.user.id
        }, status = 200)
