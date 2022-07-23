import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

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

        return JsonResponse({'results' : result}, status = 201)
        
    @signin_decorator
    def delete(self, request, cart_id):
        try:
            user = request.user
            cart = Cart.objects.get(id = cart_id, user = user)

            if not Cart.objects.filter(id = cart_id, user = user).exists():
                return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status=400)

            cart.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except Cart.DoesNotExist:
          return JsonResponse({'message' : 'CART_NOT_EXISTED'}, status=400)

        except KeyError:
          return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @signin_decorator
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            cart_id  = request.GET.get('id')
            quantity = data['quantity']

            if not Cart.objects.filter(id=cart_id, user=user).exists():
                return JsonResponse({'message' : 'INVALID_CART_ID'}, status=404)

            if quantity <= 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.quantity = quantity
            cart.save()
            return JsonResponse({'quantity' : cart.quantity}, status=200)

        except MultipleObjectsReturned:
            return JsonResponse({'message' : 'MULTIPLE_OBJECTS_RETURNED'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)