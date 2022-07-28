from django.http      import JsonResponse
from django.views     import View
from django.db.models import Min, Max

from products.models import Product, SubCategory

# Create your views here.

class SubCategoryView(View):
    def get(self, request, category_id):  
        
        subcategories = SubCategory.objects.filter(category_id=category_id)
        
        if not subcategories:
            return JsonResponse({'message':'Subcategory does not exist.'}, status=404)  
                
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
            options = product.productoption_set.all()  
                
            result = { 
                'id'             : product.id,
                'name'           : product.name,
                'number'         : product.number,
                'description'    : product.description,
                'image_url'      : product.image_url,
                'sub_category_id': product.sub_category_id,
                'options'        : [{ 
                    'size_id': option.size.id,
                    'size'   : option.size.name,
                    'price'  : option.price
                } for option in options]
            }
            
            return JsonResponse({'result':result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'Product does not exist.'}, status=404)
    
class ProductListView(View):
    def get(self, request):
        
        sort_by   = request.GET.get('sort_by')
        limit     = int(request.GET.get('limit', 20))
        offset    = int(request.GET.get('offset', 0))
        
        sort_conditions = {
            'high_price'  : '-min_price',
            'low_price'   : 'min_price',
            'newest'      : '-created_at'
        }
        
        sort_field = sort_conditions.get(sort_by, 'created_at')
        
        filter_conditions = {
            'size'     : 'productoption__size__name',
            'min_price': 'min_price__gte',
            'max_price': 'min_price__lt'
        }
        
        filter_field = {
            filter_conditions.get(key):value 
                for (key, value) in request.GET.items() 
                    if filter_conditions.get(key) 
        }
            
        products = Product.objects\
            .annotate(min_price = Min('productoption__price'))\
            .annotate(max_price = Max('productoption__price'))\
            .filter(**filter_field).order_by(sort_field)[offset:offset+limit]
        
        result = [{ 
            'id'       : product.id,
            'name'     : product.name,
            'image_url': product.image_url,
            'min_price': product.min_price,
            'max_price': product.max_price 
        } for product in products]
        
        return JsonResponse({'result':result}, status=200)   