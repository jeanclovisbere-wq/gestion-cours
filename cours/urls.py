from django.urls import path
from .views import CoursListView, CoursCreateView, CoursUpdateView, CoursDeleteView

urlpatterns = [
    path('', CoursListView.as_view(), name='cours-list'),
    path('ajouter/', CoursCreateView.as_view(), name='cours-create'),
    path('modifier/<int:pk>/', CoursUpdateView.as_view(), name='cours-update'),
    path('supprimer/<int:pk>/', CoursDeleteView.as_view(), name='cours-delete'),
]