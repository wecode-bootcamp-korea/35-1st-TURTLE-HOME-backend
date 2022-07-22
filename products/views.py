from django.http  import JsonResponse
from django.views import View

from products.models import SubCategory

# Create your views here.

class SubCategoryView(View):
    def get(self, request, category_id):  
        
        subcategories = SubCategory.objects.filter(category_id=category_id)
        result        = []
        
        if not subcategories:
            return JsonResponse({'message':'Subcategory does not exist.'}, status=400)
        
        for subcategory in subcategories:
            result.append({
                'id'         : subcategory.id,
                'name'       : subcategory.name,
                'image_url'  : subcategory.image_url,
                'category_id': category_id,
            })
        
        return JsonResponse({'result':result}, status=200)