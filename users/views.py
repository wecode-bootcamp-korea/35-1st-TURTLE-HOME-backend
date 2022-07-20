import json, re, bcrypt

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError


from users.validation import email_check, password_check
from .models import User

# Create your views here.

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_name     = data['korean_name']
            user_email    = data['email']
            user_password = data['password']
            user_address  = data['address']
            user_phone    = data['phone_number']

            email_check(user_email)

            if User.objects.filter(email=user_email).exists(): 
                return JsonResponse({'MESSAGE' : 'EXISTENT_EMAIL'}, status=400)

            if User.objects.filter(phone_number=user_phone).exists():
                return JsonResponse({'MESSAGE' : 'EXISTENT_PHONE_NUMBER'}, status=400)

            password_check(user_password)

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                korean_name  = user_name,
                email        = user_email,
                password     = hashed_password,
                address      = user_address,
                phone_number = user_phone
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        except KeyError: 
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
        except ValidationError: 
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=400)

