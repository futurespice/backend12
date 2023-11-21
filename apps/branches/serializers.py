from django.db import transaction
from rest_framework import serializers

from .models import Branch, Schedule, Workdays


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "title", "description"]


class WorkdaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workdays
        fields = ["id", "workday", "start_time", "end_time"]


class BranchSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    workdays = WorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = [
            "id",
            "image",
            "name_of_shop",
            "schedule",
            "address",
            "phone_number",
            "link_to_map",
            "workdays",
        ]

    def validate_workdays(self, value):
        for workday_data in value:
            try:
                WorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
            except serializers.ValidationError as e:
                raise serializers.ValidationError(
                    {"workdays": "Error in workday data: {}".format(e)}
                )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            schedule_data = validated_data.pop("schedule")
            schedule = Schedule.objects.create(**schedule_data)
            branch = Branch.objects.create(schedule=schedule, **validated_data)

            if "workdays" in self.initial_data:
                workdays_data = self.initial_data["workdays"]
                for workday_data in workdays_data:
                    workday_serializer = WorkdaysSerializer(data=workday_data)
                    if workday_serializer.is_valid(raise_exception=True):
                        workday = workday_serializer.save(schedule=schedule)

        return branch


class BranchCreateSerializer(serializers.ModelSerializer):
    workdays = WorkdaysSerializer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = [
            "id",
            "image",
            "name_of_shop",
            "address",
            "phone_number",
            "link_to_map",
            "workdays",
        ]

    def validate_workdays(self, value):
        for workday_data in value:
            try:
                WorkdaysSerializer(data=workday_data).is_valid(raise_exception=True)
            except serializers.ValidationError as e:
                raise serializers.ValidationError(
                    {"workdays": "Error in workday data: {}".format(e)}
                )
        return value

    def create(self, validated_data):
        with transaction.atomic():
            schedule_name = f'График работы {validated_data["address"]}'
            schedule = Schedule.objects.create(title=schedule_name)
            branch = Branch.objects.create(schedule=schedule, **validated_data)

            if "workdays" in self.initial_data:
                workdays_data = self.initial_data["workdays"]
                for workday_data in workdays_data:
                    workday_serializer = WorkdaysSerializer(data=workday_data)
                    if workday_serializer.is_valid(raise_exception=True):
                        workday = workday_serializer.save(schedule=schedule)

        return branch


class PutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["image"]
