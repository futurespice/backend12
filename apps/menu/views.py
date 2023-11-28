from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema

from apps.storage.serializers import *
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Category, Branch  # Подставьте соответствующие модели


class ChooseBranchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeBranchSerializer

    def get(self, request):
        branches = [branch.name_of_shop for branch in Branch.objects.all()]
        return Response({'branches': branches})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'branch_name': openapi.Schema(type=openapi.TYPE_STRING, description='Название филиала')
            }
        )
    )
    def post(self, request):
        user = request.user
        branch_name = request.data.get("branch_name")
        user.branch = Branch.objects.filter(name_of_shop=branch_name).first()
        user.save()

        return Response({'message': f'Выбран филиал: {user.branch.name_of_shop}'}, status=status.HTTP_200_OK)


class BranchCategoriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, branch_name):
        try:
            # Получаем филиал по имени
            branch = Branch.objects.get(name_of_shop=branch_name)
        except Branch.DoesNotExist:
            return Response({'error': 'Филиал не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем все категории для выбранного филиала
        categories = Category.objects.filter(branch=branch)

        # Пример сериализации. Замените на вашу сериализацию категорий.
        serialized_categories = CategorySerializer(categories, many=True).data

        return Response({'categories': serialized_categories}, status=status.HTTP_200_OK)


class BranchCategoriesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_categories_by_branch(self, branch_name):
        try:
            branch = Branch.objects.get(name_of_shop=branch_name)
        except Branch.DoesNotExist:
            return None

        # Получаем все товары, связанные с филиалом
        items_in_branch = Item.objects.filter(menu__branch=branch)

        # Получаем все уникальные категории, которые связаны с этими товарами
        categories = Category.objects.filter(item__in=items_in_branch).distinct()

        # Сериализация данных с использованием CategorySerializer
        serialized_categories = CategorySerializer(categories, many=True).data

        return serialized_categories

    def get(self, request, branch_name):
        # Получаем категории по филиалу
        serialized_categories = self.get_categories_by_branch(branch_name)

        if serialized_categories is not None:
            return Response({'categories': serialized_categories}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Филиал не найден'}, status=status.HTTP_404_NOT_FOUND)


class PopularItemsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_popular_items(self, branch_name):
        # Получаем 10 самых популярных продуктов (по количеству заказов) для выбранного филиала
        popular_items = (
            Item.objects
            .filter(orders__user__branch__name_of_shop=branch_name)
            .annotate(order_count=Count('orders'))
            .order_by('-order_count')[:10]
        )

        # Сериализация данных
        serialized_items = ItemSerializer(popular_items, many=True).data
        return serialized_items

    def get(self, request, branch_name):
        # Получаем популярные продукты для выбранного филиала
        serialized_items = self.get_popular_items(branch_name)
        return Response({'popular_items': serialized_items}, status=status.HTTP_200_OK)


class CategoryProductsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_products_by_category(self, branch_name, category_name):
        # Получаем продукты для выбранной категории и филиала
        products = Item.objects.filter(
            menu__branch__name_of_shop=branch_name,
            category__name=category_name
        )

        serialized_products = ItemSerializer(products, many=True).data
        return serialized_products

    def get(self, request, branch_name, category_name):
        # Получаем продукты для выбранной категории и филиала
        serialized_products = self.get_products_by_category(branch_name, category_name)

        return Response({'products': serialized_products}, status=status.HTTP_200_OK)