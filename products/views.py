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
        
        # 보내줘야할 데이터 : ID/상품명/이미지/가격들 전부    
    
        # 1. 전체 상품을 가져온다.
        # 2. 전체 상품은 여러개니까 객체들이 쿼리셋에 담아 반환된다.
        
        # 백에서 줄 때 옵션에 따른 가격들을 다 준다.
        # 대신에 가격을 정렬할 때 [10000,20000,30000,40000] 오름차순으로 정렬하면 프론트에서 인덱스값을 사용하여 최소값, 최대값 사용 가능
        # 상품 가격이 1개일 때도 [10000] 리스트에 담아서 주기로 합의함
        
        products = Product.objects.all()   # 전체 상품 객체들을 가져온다 => 여러개니까 products에 쿼리셋이 담김 => 반복문을 돌며 담기
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : [product.productoption_set.filter(product_id = product.id)[i].price for i in range(len(product.productoption_set.filter(product_id = product.id)))]} for product in products]


        return JsonResponse({'result':result}, status=200)
    
    
     