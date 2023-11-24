from django.db.models import Sum, F
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.branches.models import Branch
from apps.branches.serializers import BranchSerializer
from apps.storage.models import Item, Category, Composition, AvailableAtTheBranch
from apps.storage.serializers import ItemSerializer, CategorySerializer, CompositionSerializer
import random
from apps.accounts.models import CustomUser

from .serializers import ChangeBranchSerializer


class ChooseBranchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeBranchSerializer

    def post(self, request):
        user = request.user
        branch_id = request.data["branch_id"]
        user = CustomUser.objects.get(id=user.id)
        user.branch = Branch.objects.filter(id=branch_id).first()
        user.save()
        return Response({'message':f'{user.branch.name_of_shop}'})


class SearchProductsView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        branch_id = self.kwargs['branch_id']
        available_items = self.get_available_items(branch_id)
        return available_items

    def get_available_items(self, branch_id):
        items_requirements = Composition.objects.values(
            'item_id',
            'ingredient_id',
            'quantity'
        )

        available_quantities = AvailableAtTheBranch.objects.filter(
            branch_id=branch_id
        ).values(
            'ingredient_id'
        ).annotate(
            total_quantity=Sum('quantity')
        )

        available_dict = {a['ingredient_id']: a['total_quantity'] for a in available_quantities}

        available_items = set()
        for requirement in items_requirements:
            ingredient_id = requirement['ingredient_id']
            required_quantity = requirement['quantity']
            available_quantity = available_dict.get(ingredient_id, 0)

            if available_quantity >= required_quantity:
                available_items.add(requirement['item_id'])

        return Item.objects.filter(id__in=available_items)


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductsInCategoryView(generics.ListAPIView):
    serializer_class = CompositionSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Composition.objects.filter(item__category_id=category_id)
        return queryset


class ProductInfoView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'pk'

    def get_nice_addition(self, item):
        categories = Category.objects.all()
        nice_addition_items = []

        for category in categories:
            if item.category != category:
                items_in_category = Item.objects.filter(category=category)
                if items_in_category.exists():
                    nice_addition_items.append(random.choice(items_in_category))

        serializer = ItemSerializer(nice_addition_items, many=True)
        return serializer.data

    def get_similar_items(self, item, num_items=4):
        # Получаем продукты из текущей категории, исключая текущий продукт
        similar_items = Item.objects.filter(category=item.category).exclude(id=item.id)

        # Получаем случайные продукты из текущей категории
        if similar_items.count() > num_items:
            similar_items = random.sample(list(similar_items), num_items)

        serializer = ItemSerializer(similar_items, many=True)
        return serializer.data

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        item = self.get_object()

        # Увеличиваем счетчик просмотров
        item.views = F('views') + 1
        item.save()

        # Получаем приятное дополнение
        nice_addition = self.get_nice_addition(item)

        # Получаем похожие продукты
        similar_items = self.get_similar_items(item)

        # Добавляем информацию в ответ
        response.data['nice_addition'] = nice_addition
        response.data['similar_items'] = similar_items

        return response


class CheckIngredientsView(APIView):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        # Implement logic to check if there are enough ingredients
        # Return appropriate response
        return Response({"message": "Product is available"}, status=status.HTTP_200_OK)
