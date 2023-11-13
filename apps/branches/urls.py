from django.urls import path

from .views import BranchCreateView, BranchDeleteView, BranchListView, BranchUpdateView

urlpatterns = [
    path("", BranchListView.as_view()),  # /branches/
    path("create/", BranchCreateView.as_view()),  # /branches/create/
    path("update/<int:id>/", BranchUpdateView.as_view()),  # /branches/update/1/
    path("delete/<int:id>/", BranchDeleteView.as_view()),  # /branches/delete/1/
]
