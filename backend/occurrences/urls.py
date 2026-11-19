from django.urls import path

from . import views

app_name = "occurrences"

urlpatterns = [
    path("create/", views.OccurrenceCreateView.as_view(), name="create"),
    path("mine/", views.OccurrenceListView.as_view(), name="mine"),
    path("<int:pk>/", views.OccurrenceDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.OccurrenceUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.OccurrenceDeleteView.as_view(), name="delete"),
    path("<int:pk>/approve-return/", views.approve_return, name="approve_return"),
]
