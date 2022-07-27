import json

from django.views import View
from django.http  import JsonResponse

from .models         import Cart
from products.models import ProductOption
from core.utils      import signin_decorator

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

    @signin_decorator
    def get(self, request):
        carts = Cart.objects.filter(user = request.user)
        result = [{
            "cart_id"          : cart.id,
            "user_id"          : cart.user_id,
            "product_option_id": cart.product_option_id,
            "product_name"     : cart.product_option.product.name,
            "product_price"    : int(cart.product_option.price) * int(cart.quantity),
            "product_image"    : cart.product_option.product.image_url,
            "product_number"   : cart.product_option.product.number,
            "product_size"     : cart.product_option.size.name,
            "quantity"         : cart.quantity
        } for cart in carts]

        return JsonResponse({'results' : result}, status = 200)

    @signin_decorator
    def delete(self, request, cart_id):
        try:
            user = request.user
            cart = Cart.objects.get(id = cart_id, user = user)

            cart.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 204)

        except Cart.DoesNotExist:
          return JsonResponse({'message' : 'CART_NOT_EXISTED'}, status=404)

