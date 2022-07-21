from django.urls import path

from products.views import ProductView, SubCategoryView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/subcategories', SubCategoryView.as_view()),
]