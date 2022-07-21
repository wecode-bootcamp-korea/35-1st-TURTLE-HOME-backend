import json

from django.views     import View
from django.http      import JsonResponse

from users.models     import Cart
from products.models  import ProductOption
from users.utils      import 데코레이터

# Create your views here.

class CartView(View):
    @데코레이터
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user
            product_id = data['product_option_id']
            quantity   = data['quantity']

            if quantity <= 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            cart, is_created = Cart.objects.get_or_create(
                user_id    = user_id,
                produtc_id = product_id
            )
            cart.quantity = quantity
            cart.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @데코레이터
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user
            product_id = data['products_options_id']
            quantity   = data['quantity']
            
            cart, is_created = Cart.objects.get_or_create(
                user_id    = user_id,
                product_id = product_id
            )
            quantity =- 1
            cart.quantity =+ quantity
            cart.save()

            return JsonResponse({'message' : 'SUCCESS'}, status= 201)

        except Cart.DoesNotExist: 
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)

        except KeyError: 
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)