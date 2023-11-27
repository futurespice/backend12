from rest_framework import serializers
from apps.storage.models import Item, Ingredient, Composition, ReadyMadeProduct, AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch
from .models import *
from drf_yasg import openapi


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class RecommendedMenuSerializer(serializers.Serializer):
    category = CategorySerializer()
    items = MenuSerializer(many=True)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = "__all__"
        ref_name = "MenuCompositionSerializer"


class ReadyMadeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyMadeProduct
        fields = "__all__"


class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableAtTheBranch
        fields = "__all__"


class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = "__all__"


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




class ChooseBranchSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name_of_shop', read_only=True)

    class Meta:
        ref_name = "ChooseBranchSerializer"
        model = AvailableAtTheBranch
        fields = ['id', 'branch_name']


class PopularItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['is_available']


class MenuAdditionalDataSerializer(serializers.Serializer):
    extra_field = serializers.CharField()


class MenuSerializer(serializers.ModelSerializer):
    additional_data = MenuAdditionalDataSerializer()

    class Meta:
        model = Menu
        fields = "__all__"