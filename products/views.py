from itertools import product
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Min, Max, Q

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
    """
    목적: 상품의 목록을 반환

    조건1 - 필터
        - 사이즈
        - 가격
    조건2 - 정렬
        - 가격
        - 최신
    조건3 - 페이지네이션

    구조
    1. request로 받은 값들을 검증
    2. 로직
        - 필터
        - 정렬
        - 위의 조건을 가지고 데이터를 가져옴 + 페이지네이션
    3. response

    """
    #8000/products?size=S&size=M : getlist
    #8000/products?size=S,M : split
    def get(self, request):        
        sort_by   = request.GET.get('sort_by')
        size      = request.GET.get('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        limit     = int(request.GET.get('limit', 20))
        offset    = int(request.GET.get('offset', 0))
            
        sort_conditions = {
            'high_price'  : '-min_price',
            'low_price'   : 'min_price',
            'newest'      : '-created_at'
        }
        
        sort_field = sort_conditions.get(sort_by, 'created_at')
        
        q = Q()
        
        if size : 
            q &= Q(productoption__size__name = size)
            # q = q & Q(productoption__size__name = size)   
        if min_price:
            q.add(Q(price__gte = min_price), q.AND)
                
        if max_price or max_price != 'null':
            q.add(Q(price__lt = max_price), q.AND)   
    
        products = Product.objects\
                          .annotate(min_price = Min('productoption__price'))\
                          .annotate(max_price = Max('productoption__price'))\
                          .filter(q)\
                          .order_by(sort_field)[offset:offset+limit] 
        #QuerySet[1,2,3,5]
        # 0 10
        # 10 10
        # 20 10    
        result = [{ 
            'id'        : product.id, 
            'name'      : product.name,
            'image_url' : product.image_url,
            'min_price' : product.min_price,
            'max_price' : product.max_price
        } for product in products]  
        
        return JsonResponse({'result':result}, status=200)   