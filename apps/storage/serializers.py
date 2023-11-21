"""
Serializers for storage app.
"""
from django.db import models
from rest_framework import serializers

from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays
from apps.storage.models import (AvailableAtTheBranch, Category, Composition,
                                 Ingredient, Item, ReadyMadeProduct,
                                 ReadyMadeProductAvailableAtTheBranch, AdditionalProduct, AvailableAdditionalProduct,
                                 ItemAdditionalProduct)


# =====================================================================
# CATEGORY SERIALIZER
# =====================================================================
class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
    """

    class Meta:
        model = Category
        fields = "__all__"


# =====================================================================
# EMPLOYEE SERIALIZERS
# =====================================================================
class EmployeeWorkdaysSerializer(serializers.ModelSerializer):
    """
    EmployeeWorkdays serializer.
    """

    class Meta:
        model = EmployeeWorkdays
        fields = ["id", "workday", "start_time", "end_time"]

    def create(self, validated_data):
        """
        Create employee workdays.
        """
        employee_workdays = EmployeeWorkdays.objects.create(**validated_data)
        return employee_workdays


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    """
    EmployeeSchedule serializer for EmployeeSerializer and ScheduleUpdateSerializer.
    """

    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["id", "title", "workdays"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Employee serializer.
    """

    schedule = EmployeeScheduleSerializer()
    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
            "schedule",
            "workdays",
        ]

    def validate_workdays(self, value):
        """
        Validate workdays data.
        """
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Employee create serializer.
    """

    workdays = EmployeeWorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
            "workdays",
        ]

    def validate_workdays(self, value):
        """
        Validate workdays data.
        """
        for workday_data in value:
            EmployeeWorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
        return value

    def create(self, validated_data):
        """
        Create employee.
        """
        schedule_data = {"title": f"{validated_data['first_name']}'s schedule"}

        schedule = EmployeeSchedule.objects.create(**schedule_data)
        CustomUser.objects.create(schedule=schedule, **validated_data)

        if "workdays" in self.initial_data:
            workdays_data = self.initial_data["workdays"]
            for workday_data in workdays_data:
                workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
                if workday_serializer.is_valid(raise_exception=True):
                    workday_serializer.save(schedule=schedule)

        return CustomUser.objects.get(username=validated_data["username"])


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "position",
            "birth_date",
            "phone_number",
            "branch",
        ]

    def update(self, instance, validated_data):
        """
        Update employee.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.position = validated_data.get("position", instance.position)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.branch = validated_data.get("branch", instance.branch)
        instance.save()
        return instance


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    """
    Schedule update serializer.
    """

    workdays = EmployeeWorkdaysSerializer(many=True)

    class Meta:
        model = EmployeeSchedule
        fields = ["workdays"]

    def update(self, instance, validated_data):
        """
        Update schedule.
        """
        user_id = self.context["user_id"]
        user = CustomUser.objects.get(id=user_id)
        schedule = user.schedule

        schedule.title = f"{user.first_name}'s schedule"
        schedule.save()

        schedule.workdays.all().delete()

        workdays_data = validated_data.pop("workdays", [])

        for workday_data in workdays_data:
            workday_serializer = EmployeeWorkdaysSerializer(data=workday_data)
            if workday_serializer.is_valid(raise_exception=True):
                workday_serializer.save(schedule=schedule)

        return schedule


# =====================================================================
# INGREDIENT SERIALIZERS
# =====================================================================
class CreateAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    CreateAvailableAtTheBranch serializer.
    """

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "quantity"]


class AvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    AvailableAtTheBranch serializer.
    """

    branch = serializers.StringRelatedField()
    ingredient = serializers.StringRelatedField()

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "branch", "ingredient", "quantity"]

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["ingredient"] = instance.ingredient.name
        representation["branch"] = instance.branch.name_of_shop
        quantity = (
            round(instance.quantity / 1000, 2)
            if instance.ingredient.measurement_unit in ["kg", "l"]
            else instance.quantity
        )
        representation["quantity"] = quantity
        return representation


class CreateIngredientSerializer(serializers.ModelSerializer):
    """
    CreateIngredient serializer.
    """

    available_at_branches = CreateAvailableAtTheBranchSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "minimal_limit",
            "available_at_branches",
        ]

    def create(self, validated_data):
        """
        Create ingredient.
        """
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        ingredient = Ingredient.objects.create(**validated_data)
        for available_at_branch_data in available_at_branches_data:
            if ingredient.measurement_unit in ["kg", "l"]:
                available_at_branch_data["quantity"] *= 1000
            AvailableAtTheBranch.objects.create(
                ingredient=ingredient, **available_at_branch_data
            )
        return ingredient

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["available_at_branches"] = AvailableAtTheBranchSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=instance), many=True
        ).data
        return representation


class IngredientSerializer(serializers.ModelSerializer):
    """
    Ingredient serializer.
    """

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "minimal_limit",
            "date_of_arrival",
        ]

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        total_quantity = AvailableAtTheBranch.objects.filter(
            ingredient=instance
        ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
        
        if total_quantity is not None:
            representation["total_quantity"] = round(total_quantity / 1000, 2) if instance.measurement_unit in ["kg", "l"] else total_quantity
        else:
            representation["total_quantity"] = 0
        representation["date_of_arrival"] = instance.date_of_arrival.strftime(
            "%Y-%m-%d"
        )
        representation["available_at_branches"] = AvailableAtTheBranchSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=instance), many=True
        ).data
        return representation


class UpdateIngredientSerializer(serializers.ModelSerializer):
    """
    UpdateIngredient serializer.
    """

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "minimal_limit",
        ]


class IngredientDetailSerializer(serializers.ModelSerializer):
    """
    IngredientDetail serializer.
    """

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "measurement_unit",
            "minimal_limit",
            "date_of_arrival",
        ]

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        total_quantity = AvailableAtTheBranch.objects.filter(
            ingredient=instance
        ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
        if total_quantity is not None:
            representation["total_quantity"] = round(total_quantity / 1000, 2) if instance.measurement_unit in ["kg", "l"] else total_quantity
        else:
            representation["total_quantity"] = 0
        representation["date_of_arrival"] = instance.date_of_arrival.strftime(
            "%Y-%m-%d"
        )
        representation["available_at_branches"] = AvailableAtTheBranchSerializer(
            AvailableAtTheBranch.objects.filter(ingredient=instance), many=True
        ).data
        return representation


class AdditionalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProduct
        fields = ["id", "name", "minimal_limit", "date_of_arrival"]


class AvailableAdditionalProductSerializer(serializers.ModelSerializer):
    branch = serializers.StringRelatedField()
    additional_product = serializers.StringRelatedField()

    class Meta:
        model = AvailableAdditionalProduct
        fields = ["id", "branch", "additional_product", "quantity"]


class ItemAdditionalProductSerializer(serializers.ModelSerializer):
    additional_product = AdditionalProductSerializer()

    class Meta:
        model = ItemAdditionalProduct
        fields = ["id", "additional_product", "quantity"]


class IngredientQuantityUpdateSerializer(serializers.ModelSerializer):
    """
    IngredientQuantityUpdate serializer.
    """

    class Meta:
        model = AvailableAtTheBranch
        fields = ["id", "quantity"]

    def update(self, instance, validated_data):
        """
        Update quantity.
        """
        quantity = validated_data.get("quantity", instance.quantity)
        if instance.ingredient.measurement_unit in ["kg", "l"]:
            quantity *= 1000
        instance.quantity = quantity
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["ingredient"] = instance.ingredient.name
        representation["branch"] = instance.branch.name_of_shop
        quantity = instance.quantity
        if isinstance(quantity, str):
            quantity = float(quantity)
        quantity = (
            round(quantity / 1000, 2)
            if instance.ingredient.measurement_unit in ["kg", "l"]
            else quantity
        )
        representation["quantity"] = quantity
        return representation


# =====================================================================
# ITEM SERIALIZERS
# =====================================================================
class CompositionSerializer(serializers.ModelSerializer):
    """
    Composition serializer.
    """

    class Meta:
        model = Composition
        fields = ["id", "ingredient", "quantity"]


class CreateItemSerializer(serializers.ModelSerializer):
    """
    CreateItem serializer.
    """

    composition = CompositionSerializer(many=True, write_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",
            "composition",
            "is_available",
        ]

    def create(self, validated_data):
        """
        Create item.
        """
        composition_data = validated_data.pop("composition", [])
        item = Item.objects.create(**validated_data)
        for composition in composition_data:
            Composition.objects.create(item=item, **composition)
        return item

    def to_representation(self, instance):
        """
        Change quantity to kg or l if measurement unit is kg or l.
        """
        representation = super().to_representation(instance)
        representation["composition"] = CompositionSerializer(
            Composition.objects.filter(item=instance), many=True
        ).data
        return representation


class ItemSerializer(serializers.ModelSerializer):
    additional_products = ItemAdditionalProductSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "category", "description", "price", "image", "is_available", "additional_products"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["additional_products"] = ItemAdditionalProductSerializer(
            ItemAdditionalProduct.objects.filter(item=instance), many=True
        ).data
        return representation


class UpdateItemSerializer(serializers.ModelSerializer):
    """
    UpdateItem serializer.
    """

    compositions = CompositionSerializer(many=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image",
            "compositions",
            "is_available",
        ]

    def update(self, instance, validated_data):
        """
        Update item and compositions of item.
        """
        composition_data = validated_data.pop("compositions", [])
        instance = super().update(instance, validated_data)

        # Delete old compositions
        Composition.objects.filter(item=instance).delete()

        # Create new compositions
        for composition in composition_data:
            Composition.objects.create(item=instance, **composition)

        return instance


class PutImageToItemSerializer(serializers.ModelSerializer):
    """
    PutImageToItem serializer for ItemImageUpdateView
    """

    class Meta:
        model = Item
        fields = ["image"]


# =====================================================================
# READY MADE PRODUCT SERIALIZERS
# =====================================================================
class ReadyMadeProductAvailableAtTheBranchSerializer(serializers.ModelSerializer):
    """
    ReadyMadeProductAvailableAtTheBranch serializer.
    """

    ready_made_product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReadyMadeProductAvailableAtTheBranch
        fields = ["id", "branch", "ready_made_product", "quantity"]


class CreateReadyMadeProductSerializer(serializers.ModelSerializer):
    """
    CreateReadyMadeProduct serializer.
    """

    available_at_branches = ReadyMadeProductAvailableAtTheBranchSerializer(
        many=True, write_only=True
    )

    class Meta:
        model = ReadyMadeProduct
        fields = [
            "id",
            "name",
            "minimal_limit",
            "available_at_branches",
        ]

    def create(self, validated_data):
        """
        Create ready-made product and available at the branch.
        """
        available_at_branches_data = validated_data.pop("available_at_branches", [])
        product = ReadyMadeProduct.objects.create(**validated_data)
        for available_at_branch_data in available_at_branches_data:
            ReadyMadeProductAvailableAtTheBranch.objects.create(
                ready_made_product=product, **available_at_branch_data
            )
        return product

    def to_representation(self, instance):
        """
        Create ready-made product and available at the branch representation.
        """
        representation = super().to_representation(instance)
        representation[
            "available_at_branches"
        ] = ReadyMadeProductAvailableAtTheBranchSerializer(
            ReadyMadeProductAvailableAtTheBranch.objects.filter(
                ready_made_product=instance
            ),
            many=True,
        ).data
        representation["total_quantity"] = (
            ReadyMadeProductAvailableAtTheBranch.objects.filter(
                ready_made_product=instance
            ).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"]
            or 0
        )
        return representation


class ReadyMadeProductSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = ReadyMadeProduct
        fields = ["id", "name", "minimal_limit", "date_of_arrival", "total_quantity"]

    def get_total_quantity(self, instance):
        # Рассчитаем общее количество готового продукта на всех филиалах
        return instance.ready_made_product_available_at_the_branch.aggregate(total_quantity=models.Sum("quantity"))["total_quantity"] or 0

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Добавим поле is_available в представление
        data['is_available'] = instance.is_available()
        return data
