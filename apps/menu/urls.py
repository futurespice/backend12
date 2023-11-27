from django.urls import path
from .views import ChooseBranchView, SearchProductsView, PopularItemsView


urlpatterns = [
    path('choose-branch/', ChooseBranchView.as_view(), name='choose-branch'),
    path('search-products/<int:branch_id>', SearchProductsView.as_view(), name='search-products'),
    path('popular-items/', PopularItemsView.as_view(), name='popular-items')
    # Добавьте другие необходимые пути
]