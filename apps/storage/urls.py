from django.urls import path

from apps.storage.views import (
    CreateCategoryView,
    CreateEmployeeView,
    CreateIngredientView,
    CreateItemView,
    DestroyCategoryView,
    EmployeeDestroyView,
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
    IngredientDestroyView,
    IngredientDetailView,
    IngredientListView,
    IngredientQuantityUpdateView,
    InredientDestroyFromBranchView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
    ListCategoryView,
    ItemDestroyView,
    PutImageToItemView,
    ScheduleUpdateView,
    UpdateCategoryView,
    UpdateIngredientView,
    ReadyMadeProductCreateView,
    ReadyMadeProductDestroyView,
    ReadyMadeProductListView,
    ReadyMadeProductDetailView,
    ReadyMadeProductUpdateView,
    ReadyMadeProductQuantityUpdateView,
)

# Category URLs
urlpatterns = [
    path("categories/", ListCategoryView.as_view()),
    path("categories/create/", CreateCategoryView.as_view()),
    path("categories/destroy/<int:pk>/", DestroyCategoryView.as_view()),
    path("categories/update/<int:pk>/", UpdateCategoryView.as_view()),
]

# Employee URLs
urlpatterns += [
    path("employees/create/", CreateEmployeeView.as_view()),
    path("employees/", EmployeeListView.as_view()),
    path("employees/<int:pk>/", EmployeeDetailView.as_view()),
    path("employees/update/<int:pk>/", EmployeeUpdateView.as_view()),
    path("employees/schedule/update/<int:pk>/", ScheduleUpdateView.as_view()),
    path("employees/destroy/<int:pk>/", EmployeeDestroyView.as_view()),
]

# Ingredient URLs
urlpatterns += [
    path("ingredients/create/", CreateIngredientView.as_view()),
    path("ingredients/update/<int:pk>/", UpdateIngredientView.as_view()),
    path("ingredients/<int:pk>/", IngredientDetailView.as_view()),
    path("ingredients/destroy/<int:pk>/", IngredientDestroyView.as_view()),
    path("ingredients/", IngredientListView.as_view()),
    path("ingredient-quantity-update/<int:id>/", IngredientQuantityUpdateView.as_view()),
    path("ingredient-destroy-from-branch/<int:pk>/", InredientDestroyFromBranchView.as_view()),
]

# Item URLs
urlpatterns += [
    path("items/create/", CreateItemView.as_view()),
    path("items/", ItemListView.as_view()),
    path("items/<int:pk>/", ItemDetailView.as_view()),
    path("items/update/<int:pk>/", ItemUpdateView.as_view()),
    path("put-image-to-item/<int:pk>/", PutImageToItemView.as_view()),
    path("items/destroy/<int:pk>/", ItemDestroyView.as_view()),
]

# Ready-made product URLs
urlpatterns += [
    path("ready-made-products/create/", ReadyMadeProductCreateView.as_view()),
    path("ready-made-products/", ReadyMadeProductListView.as_view()),
    path("ready-made-products/<int:pk>/", ReadyMadeProductListView.as_view()),
    path("ready-made-products/destroy/<int:pk>/", ReadyMadeProductDestroyView.as_view()),
    path("ready-made-products/update/<int:pk>/", ReadyMadeProductUpdateView.as_view()),
    path("ready-made-products/quantity-update/<int:id>/", ReadyMadeProductQuantityUpdateView.as_view()),
    path("ready-made-products/<int:pk>/", ReadyMadeProductDetailView.as_view()),
]
