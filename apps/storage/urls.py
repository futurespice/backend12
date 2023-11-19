from django.urls import path

from apps.storage.views import (CreateCategoryView, CreateEmployeeView,
                                CreateIngredientView, CreateItemView,
                                DestroyCategoryView, EmployeeDestroyView,
                                EmployeeDetailView, EmployeeListView,
                                EmployeeUpdateView, IngredientDestroyView,
                                IngredientDetailView, IngredientListView,
                                IngredientQuantityUpdateView,
                                InredientDestroyFromBranchView, ItemDetailView,
                                ItemListView, ItemUpdateView, ListCategoryView,
                                PutImageToItemView, ReadyMadeProductCreateView,
                                ReadyMadeProductListView, ScheduleUpdateView,
                                UpdateCategoryView, UpdateIngredientView,
                                ItemDestroyView,)

urlpatterns = [
    path("categories/", ListCategoryView.as_view()),  # storage/categories/
    path(
        "categories/create/", CreateCategoryView.as_view()
    ),  # storage/categories/create/
    path(
        "categories/destroy/<int:pk>/", DestroyCategoryView.as_view()
    ),  # storage/categories/destroy/<int:pk>/
    path(
        "categories/update/<int:pk>/", UpdateCategoryView.as_view()
    ),  # storage/categories/update/<int:pk>/
    path(
        "employees/create/", CreateEmployeeView.as_view()
    ),  # storage/employees/create/
    path("employees/", EmployeeListView.as_view()),  # storage/employees/
    path(
        "employees/<int:pk>/", EmployeeDetailView.as_view()
    ),  # storage/employees/<int:pk>/
    path(
        "employees/update/<int:pk>/", EmployeeUpdateView.as_view()
    ),  # storage/employees/update/<int:pk>/
    path(
        "employees/schedule/update/<int:pk>/", ScheduleUpdateView.as_view()
    ),  # storage/employees/schedule/update/<int:pk>/
    path(
        "employees/destroy/<int:pk>/", EmployeeDestroyView.as_view()
    ),  # storage/employees/destroy/<int:pk>/
    path(
        "ingredients/create/", CreateIngredientView.as_view()
    ),  # storage/ingredients/create/
    path(
        "ingredients/update/<int:pk>/", UpdateIngredientView.as_view()
    ),  # storage/ingredients/update/<int:pk>/
    path(
        "ingredients/<int:pk>/", IngredientDetailView.as_view()
    ),  # storage/ingredients/<int:pk>/
    path(
        "ingredients/destroy/<int:pk>/", IngredientDestroyView.as_view()
    ),  # storage/ingredients/destroy/<int:pk>/
    path("ingredients/", IngredientListView.as_view()),  # storage/ingredients/
    path(
        "ingredient-quantity-update/<int:id>/",
        IngredientQuantityUpdateView.as_view(),
    ),  # storage/ingredient-quantity-update/<int:pk>/
    path(
        "ingredient-destroy-from-branch/<int:pk>/",
        InredientDestroyFromBranchView.as_view(),
    ),  # storage/ingredient-destroy-from-branch/<int:pk>/
    path("items/create/", CreateItemView.as_view()),  # storage/items/create/
    path("items/", ItemListView.as_view()),  # storage/items/
    path("items/<int:pk>/", ItemDetailView.as_view()),  # storage/items/<int:pk>/
    path(
        "items/update/<int:pk>/", ItemUpdateView.as_view()
    ),  # storage/items/update/<int:pk>/
    path(
        "items/destroy/<int:pk>/", ItemDestroyView.as_view()
    ),  # storage/items/destroy/<int:pk>/
    path(
        "ready-made-products/create/", ReadyMadeProductCreateView.as_view()
    ),  # storage/ready-made-products/create/
    path(
        "ready-made-products/", ReadyMadeProductListView.as_view()
    ),  # storage/ready-made-products/
    path(
        "ready-made-products/<int:pk>/", ReadyMadeProductListView.as_view()
    ),  # storage/ready-made-products/<int:pk>/
    path(
        "put-image-to-item/<int:pk>/", PutImageToItemView.as_view()
    ),  # storage/put-image-to-item/<int:pk>/
]
