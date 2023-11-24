from rest_framework import serializers
from apps.storage.models import Item, Ingredient, Composition, ReadyMadeProduct, AvailableAtTheBranch, ReadyMadeProductAvailableAtTheBranch


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
    branch_id = serializers.IntegerField(required=True)