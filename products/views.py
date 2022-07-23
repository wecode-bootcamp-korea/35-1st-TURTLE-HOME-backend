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
        
        sorting = request.GET.get('sort-by')   # get메소드는 해당 키값에 대한 벨류값이 없을 경우 None을 리턴한다
        
        # 정렬은 중복선택 안됨 -> 낮은가격/높은가격/최신에 따른 분기처리 각각하기
        
        # 낮은 가격순 => price
        if sorting == 'price':
            pass
        
        
        # 높은 가격순 => -price
        elif sorting == '-price':
            pass
        
        # 최신 등록순 => -id
        elif sorting == '-id':
            products = Product.objects.all().order_by('-created_at')
            
            result = [{ 'id'       : product.id, 
                        'name'     : product.name,
                        'image_url': product.image_url,
                        'prices'   : [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                    } for product in products] 
            
            return JsonResponse({'message':'Ordering by newest', 'result':result}, status=200)
        
        # 일반
        products = Product.objects.all()   
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : 
                        [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                    } for product in products] 

        return JsonResponse({'result':result}, status=200)
    
    
     