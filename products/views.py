from django.http  import JsonResponse
from django.views import View

from products.models import Product, SubCategory

# Create your views here.

class SubCategoryView(View):
    def get(self, request, category_id):  
        
        subcategories = SubCategory.objects.filter(category_id=category_id)
        
        if not subcategories:
            return JsonResponse({'message':'Subcategory does not exist.'}, status=400)
        
        result = [{ 
                    'id'         : subcategory.id,
                    'name'       : subcategory.name,
                    'image_url'  : subcategory.image_url,
                    'category_id': category_id } for subcategory in subcategories]
        
        return JsonResponse({'result':result}, status=200)    
     
class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)   
            options = product.productoption_set.filter(product_id = product.id)  
            
            result = { 'id'              : product.id,
                        'name'           : product.name,
                        'number'         : product.number,
                        'description'    : product.description,
                        'image_url'      : product.image_url,
                        'sub_category_id': product.sub_category_id,
                        'options'        : [{ 'size':option.size.name,
                                             'price':option.price } for option in options]}
            
            return JsonResponse({'result':result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'Product does not exist.'}, status=404)