from django.http      import JsonResponse
from django.views     import View
from django.db.models import F

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
        
        sort_condition = request.GET.get('sort-by')   # get메소드는 해당 키값에 대한 벨류값이 없을 경우 None을 리턴한다
        
        # 정렬은 중복선택 안됨 -> 낮은가격/높은가격/최신에 따른 분기처리 각각하기
        
        # 낮은 가격순 => price
        if sort_condition == 'price':
            # sort_by_lowprice = ProductOption.objects.all().order_by('price')
            # a = [t for t in sort_by_lowprice]
            # print(a)
            
            # price_with_name= sort_by_lowprice.prefetch_related('product__name')
            # print(price_with_name)
            
            # print([product.productoption_set.filter(product_id = product.id) for product in products])  # 상품과 가격이 연결되었음
            # test = [product.productoption_set.filter(product_id = product.id) for product in products]
            # test = products.annotate(price = ProductPrice('productoption')).order_by('-price')
            
            # test = ProductOption.objects.values('price', 'product__id', 'product__name', 'product__image_url')
            # print(test)    => 1개의 상품에 4개의 가격이 나와야하는데 가격이 모두 다르니까 4개의 객체가 생성된다.
            
            
            # ----- 1번째 방법 : 상품옵션 객체를 하나하나 다 쪼갰고 거기에 이름을 붙여서 보내주고 있음
            # product_options = ProductOption.objects.annotate(name=F('product__name'), image_url=F('product__image_url'), p_id=F('product__id')).order_by('-price')  # 상품이름과 옵션테이블 연결하기
            # result          = [{ 'product_id' : product.p_id, 
            #                      'name'       : product.name,
            #                      'image_url'  : product.image_url,
            #                      'price'      : [product.price ]} for product in product_options]

            # return JsonResponse({'message':'Ordering by highest price', 'result':result}, status=200)
            
            # ----- 2번째 방법 : 하나의 상품안에 여러가지 가격들이 담겨있다. 그 가격들은 정렬되어 있음. 그 정렬된 가격들 중에서 [0]기준 [-1]기준으로, 그 값들을 정렬해서 보내주자.
            products =  Product.objects.all()
            
            result = [{ 'id'       : product.id, 
                        'name'     : product.name,
                        'image_url': product.image_url,
                        'prices'   : 
                            [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                        } for product in products] 
        
            sorted_result = sorted(result, key = lambda x : x['prices'][0])
        
            return JsonResponse({'message':'Ordered by lowest price', 'result':sorted_result}, status=200)
        
        
        # 높은 가격순 => -price
        elif sort_condition == '-price':
            pass
        
        # 최신 등록순 => -id
        elif sort_condition == '-id':
            products = Product.objects.all().order_by('-created_at')
            
            result = [{ 'id'       : product.id, 
                        'name'     : product.name,
                        'image_url': product.image_url,
                        'prices'   : 
                            [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                        } for product in products] 
            
            return JsonResponse({'message':'Ordered by newest', 'result':result}, status=200)
        
        # 일반
        products = Product.objects.all()   
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : 
                        [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                    } for product in products] 

        return JsonResponse({'result':result}, status=200)
    
    
     