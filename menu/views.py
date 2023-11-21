from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from apps.branches.models import Branch
from apps.branches.serializers import BranchSerializer
from apps.storage.models import Item, Category, Composition
from apps.storage.serializers import ItemSerializer, CategorySerializer, CompositionSerializer


class ChooseBranchView(APIView):
    def get(self, request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchProductsView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        branch_id = self.kwargs['branch_id']  # Assuming the branch_id is passed in the URL
        # Implement your filtering logic based on branch_id, category, and popularity
        queryset = Item.objects.filter(branch_id=branch_id)
        return queryset


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductsInCategoryView(generics.ListAPIView):
    serializer_class = CompositionSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        # Implement your filtering logic based on the category_id
        queryset = Composition.objects.filter(item__category_id=category_id)
        return queryset


class ProductInfoView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'item_id'  # Assuming you have a proper lookup field

    # Add logic for recommendation retrieval
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Implement logic to get and append recommendations to the response data
        return response


class CheckIngredientsView(APIView):
    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        # Implement logic to check if there are enough ingredients
        # Return appropriate response
        return Response({"message": "Product is available"}, status=status.HTTP_200_OK)
