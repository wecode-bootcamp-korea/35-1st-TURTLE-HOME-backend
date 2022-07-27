import json

from django.views import View
from django.http  import JsonResponse

from .models         import Cart
from core.utils      import signin_decorator
from products.models import ProductOption

# Create your views here.

class CartView(View):
    @signin_decorator
    def post(self, request):
        try:
            data              = json.loads(request.body)
            user              = request.user
            product_id        = data['product_id']
            size_id           = data['size_id']
            quantity          = int(data['quantity'])

            if quantity <= 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            if not ProductOption.objects.filter(product_id=product_id, size_id=size_id).exists():
                return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

            product_option = ProductOption.objects.get(product_id=product_id, size_id=size_id)
            
            cart, is_created = Cart.objects.get_or_create(
                user           = user,
                product_option = product_option
            )
            cart.quantity = cart.quantity + quantity
            cart.save()

            status = 201 if is_created else 200
            
            return JsonResponse({'message' : 'SUCCESS'}, status=status)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)