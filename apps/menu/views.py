from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum, F, Q
import  re
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.branches.models import Branch
from apps.branches.serializers import BranchSerializer
from apps.storage.models import Item, Category, Composition, AvailableAtTheBranch
from apps.storage.serializers import (
    ItemSerializer,
    CompositionSerializer,
    ReadyMadeProductSerializer,
)
from apps.accounts.models import CustomUser
from drf_yasg import openapi
from .serializers import *
from rest_framework.decorators import api_view
from .models import *
from django.contrib.sessions.models import Session

class ChooseBranchView(APIView):
    permission_classes = [permissions.AllowAny]
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

        # Сохраняем информацию о выбранном филиале в сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.save()

        Session.objects.filter(session_key=session_key).update(data={'branch_id': user.branch.id})

        return Response({'message': f'Выбран филиал: {user.branch.name_of_shop}'}, status=status.HTTP_200_OK)


class SearchProductsView(APIView):
    serializer_class = ItemSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('product_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Название продукта'),
        ]
    )
    def get(self, request):
        try:
            product_name = request.query_params.get('product_name', '')
            if not (1 <= len(product_name) <= 100 and re.match("^[а-яА-Я\s.,+\-!0-9]+$", product_name)):
                return Response({'error': 'Invalid input for product_name'}, status=status.HTTP_400_BAD_REQUEST)

            # Используем branch_id из сессии
            session_key = request.session.session_key
            branch_id = Session.objects.get(session_key=session_key).get_decoded().get('branch_id')

            # Выбираем только необходимые поля
            queryset = Item.objects.filter(
                category_id=branch_id
            ).values('name', 'title', 'price', 'image')

            if product_name:
                search_query = Q(name__icontains=product_name) | Q(description__icontains=product_name) | Q(
                    category__name__icontains=product_name)
                queryset = queryset.filter(search_query)

            return Response(queryset, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PopularItemsView(generics.ListAPIView):
    serializer_class = PopularItemSerializer

    def get_queryset(self):
        # Получаем популярные продукты по количеству заказов
        queryset = Item.objects.filter(is_available=True).order_by('-orders_count')[:5]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
