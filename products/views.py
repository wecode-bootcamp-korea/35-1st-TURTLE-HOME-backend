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
        
        sort_condition  = request.GET.get('sort-by')
        size_conditions = request.GET.getlist('size')
            
        products = Product.objects.all()   
            
        result = [{ 'id'       : product.id, 
                    'name'     : product.name,
                    'image_url': product.image_url,
                    'prices'   : 
                        [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                    } for product in products] 
        
        if sort_condition == 'price':
                    
            if size_conditions: 
                
                products = products.filter(productoption__size__name__in=size_conditions).order_by('id').distinct()

                result = [{ 'id'       : product.id, 
                            'name'     : product.name,
                            'image_url': product.image_url,
                            'prices'   : 
                                    [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                            } for product in products] 
                    
            result = sorted(result, key = lambda x : x['prices'][0])
        
        elif sort_condition == '-price':
            
            if size_conditions:  
                
                products = products.filter(productoption__size__name__in=size_conditions).order_by('id').distinct()

                result = [{ 'id'       : product.id, 
                            'name'     : product.name,
                            'image_url': product.image_url,
                            'prices'   : 
                                    [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                            } for product in products] 
        
            result = sorted(result, key = lambda x : x['prices'][-1], reverse=True)
    
        elif sort_condition == '-id':
            
            if size_conditions: 
                
                products = products.filter(productoption__size__name__in=size_conditions).order_by('id').distinct()

                result = [{ 'id'       : product.id, 
                            'name'     : product.name,
                            'image_url': product.image_url,
                            'prices'   : 
                                    [int(p.price) for p in product.productoption_set.filter(product_id = product.id)]
                            } for product in products] 
            
            result = sorted(result, key = lambda x : x['id'], reverse=True)
        
        return JsonResponse({'result':result}, status=200)
        
    
    
     