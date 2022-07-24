from django.http      import JsonResponse
from django.views     import View

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
        
        sort_condition = request.GET.get('sort-by')   
        
        products = Product.objects.all()   
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : 
                        [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                    } for product in products] 
        
        if sort_condition == 'price':
                    
            sorted_result = sorted(result, key = lambda x : x['prices'][0])
        
            return JsonResponse({'message':'Ordered by lowest price', 'result':sorted_result}, status=200)
        
        elif sort_condition == '-price':
        
            sorted_result = sorted(result, key = lambda x : x['prices'][0], reverse=True)
        
            return JsonResponse({'message':'Ordered by highest price', 'result':sorted_result}, status=200)
        
        elif sort_condition == '-id':
            
            # created_at이라는 값을 사용해서 정렬하자니 코드의 중복?이 생기는 데 이 코드도 줄이고 싶다.
            # products = products.order_by('-created_at')
            
            # sorted_result = [{  'id'       : product.id, 
            #                     'name'     : product.name,
            #                     'image_url': product.image_url,
            #                     'prices'   : 
            #                         [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
            #                     } for product in products] 
            
            # id도 생성한 순서대로 생기는 고유값이니까 이를 이용해서 역순으로 정렬하면 최신순이 된다!.
            sorted_result = sorted(result, key = lambda x : x['id'], reverse=True)
            
            return JsonResponse({'message':'Ordered by newest', 'result':sorted_result}, status=200)
        
        return JsonResponse({'result':result}, status=200)
    
    
     