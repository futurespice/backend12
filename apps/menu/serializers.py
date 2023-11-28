from rest_framework import serializers
from apps.storage.models import Item, Ingredient, Composition, ReadyMadeProduct, AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch
from .models import *
from drf_yasg import openapi


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'











class ChangeBranchSerializer(serializers.Serializer):
    branch_name = serializers.CharField(required=True)

    @staticmethod
    def get_parameters():
        """
        Метод для получения параметров для использования в swagger_auto_schema.
        """
        return [
            openapi.Parameter(
                'branch_name',  # Имя параметра
                openapi.IN_QUERY,  # Тип параметра (в данном случае, в запросе)
                description='Название филиала',
                type=openapi.TYPE_STRING,
            ),
        ]






