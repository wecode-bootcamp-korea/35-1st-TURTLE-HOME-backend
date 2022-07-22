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
    
class ProductListView(View):
    def get(self, request):
        
        # 상품이름과 최저가 최고가가 나와야한다. 
        # 하지만 옵션명은 필요가 없어
        # products = Product.objects.all()    # 객체가 아닌 쿼리셋!!!
        # product = [ product.productoption_set.filter(product_id = [product.id for product in products])    for product in products]
        
        # prices = products.productoption_set.filter(product_id = [product.id for product in products])
        # print(product)
        # result = [product.name  for product in products]
        
    
    
    
        # 1. 전체 상품을 가져온다.
        # 2. 전체상품을 가져오면, 여러개니까 객체가 쿼리셋에 담겨있음
        
        # 백에서 줄때 가격자체를 옵션에 따라 다 준다
        # 대신에 가격을 정렬해서 주면 프론트에서 0번째 최소가격, 마지막꺼는 최대가격
        # 1. 상품가격이 1개일때 분기처리, 여러개일떄 분기처리를 해서 줘야하고.

        products = Product.objects.all()    # 객체들이 쿼리셋으로 products에 담겨있다.
        
        a = [product.productoption_set.all()  for product in products]
        print(a)    # _set을 .name으로 사용 못함. 쿼리셋
        print(a.price)
        
        # result = [{'name':product.name,
        #            'id'   : product.id,
        #            'price': product.productoption_set.price} for product in products]
        
        

        return JsonResponse({'result':'test'}, status=200)