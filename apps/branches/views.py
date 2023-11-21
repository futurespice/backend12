from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Branch
from .serializers import BranchCreateSerializer, BranchSerializer, PutImageSerializer


class BranchListView(ListAPIView):
    manual_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "image": openapi.Schema(
                type=openapi.TYPE_STRING, description="Path to image"
            ),
            "name_of_shop": openapi.Schema(type=openapi.TYPE_STRING),
            "schedule": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "address": openapi.Schema(type=openapi.TYPE_STRING),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "link_to_map": openapi.Schema(type=openapi.TYPE_STRING),
            "workdays": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "workday": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Get branches",
        operation_description="Use this method to get branches",
        responses={200: manual_response_schema},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchCreateView(CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchCreateSerializer
    permission_classes = [IsAdminUser]

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image": openapi.Schema(
                type=openapi.TYPE_STRING, description="Path to image"
            ),
            "address": openapi.Schema(type=openapi.TYPE_STRING),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "name_of_shop": openapi.Schema(type=openapi.TYPE_STRING),
            "link_to_map": openapi.Schema(type=openapi.TYPE_STRING),
            "workdays": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "workday": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Create branch",
        operation_description="Use this method to create a branch. You must be an admin to do this.",
        request_body=manual_request_schema,
        responses={200: BranchCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BranchUpdateView(UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = "id"

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image": openapi.Schema(
                type=openapi.TYPE_STRING, description="Path to image"
            ),
            "schedule": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "address": openapi.Schema(type=openapi.TYPE_STRING),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            "name_of_shop": openapi.Schema(type=openapi.TYPE_STRING),
            "link_to_map": openapi.Schema(type=openapi.TYPE_STRING),
            "workdays": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "workday": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )

    @swagger_auto_schema(
        operation_summary="Update branch",
        operation_description="Use this method to update a branch",
        request_body=manual_request_schema,
        responses={200: BranchSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class BranchDeleteView(generics.DestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = "id"

    manual_parameters = [
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="Branch id",
        )
    ]

    @swagger_auto_schema(
        operation_summary="Delete branch",
        operation_description="Use this method to delete a branch",
        manual_parameters=manual_parameters,
        responses={200: BranchSerializer},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BranchDetailView(generics.RetrieveAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = "id"

    manual_parameters = [
        openapi.Parameter(
            name="id",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_INTEGER,
            description="Branch id",
        )
    ]

    @swagger_auto_schema(
        operation_summary="Get branch",
        operation_description="Use this method to get a branch",
        manual_parameters=manual_parameters,
        responses={200: BranchSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PutImageBranchView(UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = PutImageSerializer
    lookup_field = "id"

    manual_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"image": openapi.Schema(type=openapi.TYPE_FILE)},
    )

    @swagger_auto_schema(
        operation_summary="Put image to branch",
        operation_description="Use this method to put image to branch",
        request_body=manual_request_schema,
        responses={200: PutImageSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)