from django.urls import path
from .views import ChooseBranchView, PopularItemsListView, BranchCategoriesListView, CategoryProductsListView

app_name = 'menu'

urlpatterns = [
    path('choose-branch/', ChooseBranchView.as_view(), name='choose-branch'),
    path('popular-items/<str:branch_name>/', PopularItemsListView.as_view(), name='popular-items'),
    path('branch-categories/<str:branch_name>/', BranchCategoriesListView.as_view(), name='branch-categories'),
    path('category-products/<str:branch_name>/<str:category_name>/', CategoryProductsListView.as_view(), name='category-products'),
    # Другие URL-маршруты вашего приложения
]
