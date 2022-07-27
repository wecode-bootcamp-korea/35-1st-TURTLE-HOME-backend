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
    목적 : 상품의 목록을 반환한다.
    
    조건 : 
    1. 필터(사이즈,가격)
    2. 정렬(낮은 가격순, 높은 가격순, 최신순)
    3. 페이지네이션 (목록을 주는건 페이지네이션이 필요하다) 데이터의 부하를 막기 위해서 리스트를 줄 때 무조건 필요하다. db에서목록을 가져올땐 페이지네이션 걸기    
    
    => 먼저 쉬운 작업 후 조건을 하나씩 걸어보기
    
    구조 : 
    1. request로 받은 값들을 먼저 검증한다.  => key에러 발생해보고 아래 로직 안가도 걸를 수 있도록!!
    2. 로직 짜고
      - 필터
      - 정렬
      - 위의 조건을 가지고 데이터를 가져옴 + 페이지네이션
    3. response 주기
    """
    def get(self, request):
        
        sort_by   = request.GET.get('sort_by')
        size      = request.GET.get('size')
        min_price = request.GET.get('min_price', 0)
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
        
        products = Product.objects\
            .annotate(min_price = Min('productoption__price'))\
            .annotate(max_price = Max('productoption__price'))
        
        if size: 
            q &= Q(productoption__size__name = size)
        
        q.add(Q(min_price__gte = min_price), q.AND)
                
        if max_price :
            q.add(Q(min_price__lt = max_price), q.AND)   
            
        products = products.filter(q).order_by(sort_field)[offset:offset+limit]
        
        result = [{ 
            'id'       : product.id,
            'name'     : product.name,
            'image_url': product.image_url,
            'min_price': product.min_price,
            'max_price': product.max_price 
        } for product in products]
        
        return JsonResponse({'result':result}, status=200)   