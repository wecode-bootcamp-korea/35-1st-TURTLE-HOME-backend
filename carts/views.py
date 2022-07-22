import json

from django.views     import View
from django.http      import JsonResponse

from .models          import Cart
from core.utils       import signin_decorator

# Create your views here.

class CartView(View):
    @signin_decorator
    def post(self, request):
        try:
            data              = json.loads(request.body)
            user              = request.user
            product_option_id = data['product_option_id']
            quantity          = int(data['quantity'])

            if quantity <= 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            cart, is_created = Cart.objects.get_or_create(
                user              = user,
                product_option_id = product_option_id
            )
            cart.quantity = cart.quantity + quantity
            cart.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)