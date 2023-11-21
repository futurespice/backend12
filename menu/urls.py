from django.urls import path
from .views import *

urlpatterns = [
    path('choose-branch/', ChooseBranchView.as_view(), name='choose-branch'),
    path('search-products/<int:branch_id>/', SearchProductsView.as_view(), name='search-products'),
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('products-in-category/<int:category_id>/', ProductsInCategoryView.as_view(), name='products-in-category'),
    path('product-info/<int:product_id>/', ProductInfoView.as_view(), name='product-info'),
    path('check-ingredients/<int:product_id>/', CheckIngredientsView.as_view(), name='check-ingredients'),
]
