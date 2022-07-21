from django.http  import JsonResponse
from django.views import View

from products.models import Product, SubCategory

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
        
        return JsonResponse({'message':result}, status=200)
    
class ProductDetailView(View):
    def get(self, request, product_id):
        
        try:
            product = Product.objects.get(id=product_id)   
            options = product.productoption_set.filter(product_id = product.id)  
            
            option_list = []
            
            for option in options:
                option_list.append({
                    'size' : option.size.name,   
                    'price' : option.price
                })
            
            result = {
                'id'             : product.id,
                'name'           : product.name,
                'number'         : product.number,
                'description'    : product.description,
                'image_url'      : product.image_url,
                'sub_category_id': product.sub_category_id,
                'options'        : option_list,
            }
            
            return JsonResponse({'message':result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'Product does not exist.'}, status=400)