from django.http      import JsonResponse
from django.views     import View
from django.db.models import Min, Q

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
                    'size'  : option.size.name,
                    'price' : option.price 
                } for option in options]
            }
            
            return JsonResponse({'result':result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message':'Product does not exist.'}, status=404)
    
class ProductListView(View):
    def get(self, request):
        
        sort_by   = request.GET.get('sort_by')
        size      = request.GET.get('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        products   = Product.objects.annotate(price = Min('productoption__price'))
        
        sort_conditions = {
            'high_price'  : '-price',
            'low_price'   : 'price',
            'newest'      : '-created_at'
        }
        
        sort_field = sort_conditions.get(sort_by, 'created_at')
        
        q = Q()
        
        if size : 
            q &= Q(productoption__size__name = size)
        if min_price:
            q.add(Q(price__gte = min_price), q.AND)
                
        if max_price:
            q.add(Q(price__lt = max_price), q.AND)   
    
        products = products.filter(q).order_by(sort_field)
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : 
                        [int(p.price) for p in product.productoption_set.all()] 
                    } for product in products]  
        
        return JsonResponse({'result':result}, status=200)   