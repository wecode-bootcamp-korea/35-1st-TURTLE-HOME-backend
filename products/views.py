from django.http  import JsonResponse
from django.views import View

from products.models import SubCategory, Product

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
        

class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        result   = []
        
        for product in products:
            result.append({
                'id'             : product.id,
                'name'           : product.name,
                'number'         : product.number,
                'description'    : product.description,
                'image_url'      : product.image_url,
                'sub_category_id': product.sub_category_id
            })
        
        return JsonResponse({'message':result}, status=200)