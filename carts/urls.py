from django.urls import path

from carts.views import CartView, CartDeleteView

urlpatterns = [
    path("/cart", CartView.as_view()),
    path("/cart/<str:cart_id>", CartDeleteView.as_view())
]