from django.urls import path
from products.views import SubCategoryView

urlpatterns = [
    path('/subcategories', SubCategoryView.as_view())
    
]