from django.http  import JsonResponse
from django.views import View

from products.models import SubCategory

# Create your views here.
class SubCategoryView(View):
    def get(self, request):
        subcategories = SubCategory.objects.all()
        result        = []
        
        for subcategory in subcategories:
            result.append({
                'id'         : subcategory.id,
                'name'       : subcategory.name,
                'image_url'  : subcategory.image_url,
                'category_id': subcategory.category_id,
            })
        
        return JsonResponse({'message':result}, status=200)
        
        
    