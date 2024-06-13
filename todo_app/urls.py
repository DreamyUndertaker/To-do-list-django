from django.urls import path
from .views import (
    ListListView,
    ItemListView,
    ListCreate,
    ItemCreate,
    ItemUpdate,
    ListDelete,
    ItemDelete, OverdueItemListView,
)

urlpatterns = [
    path('', ListListView.as_view(), name='index'),
    path('list/add/', ListCreate.as_view(), name='list-add'),
    path('list/<int:list_id>/', ItemListView.as_view(), name='list'),
    path('list/<int:list_id>/item/add/', ItemCreate.as_view(), name='item-add'),
    path('list/<int:list_id>/item/<int:pk>/edit/', ItemUpdate.as_view(), name='item-update'),
    path('list/<int:list_id>/item/<int:pk>/delete/', ItemDelete.as_view(), name='item-delete'),
    path('list/<int:pk>/delete/', ListDelete.as_view(), name='list-delete'),
    path("overdue/", OverdueItemListView.as_view(), name="overdue-list"),
]
