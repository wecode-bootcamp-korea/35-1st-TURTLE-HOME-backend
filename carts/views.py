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
            data       = json.loads(request.body)
            user       = request.user #토큰으로 확인후 인증이된 유저
            product_id = data['product_option_id'] # 클라이언트가 요청하는 값
            quantity   = int(data['quantity'])

            if quantity <= 0: #수량이 정수가 아니면 에러 반환
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)

            cart, is_created = Cart.objects.get_or_create(
                user              = user,
                product_option_id = product_id # 클라이언트가 요청한 값이 있는 변수를 option_id로 변환해서 카트에 값을 저장
            )
            cart.quantity = cart.quantity + quantity
            cart.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)