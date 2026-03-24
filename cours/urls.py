from django.urls import path
from .views import AccueilView, DashboardView, CoursListView, CoursCreateView, CoursUpdateView, CoursDeleteView, imprimer_cours_pdf

urlpatterns = [
    path('', AccueilView.as_view(), name='accueil'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('liste/', CoursListView.as_view(), name='cours-list'),
    path('ajouter/', CoursCreateView.as_view(), name='cours-create'),
    path('modifier/<int:pk>/', CoursUpdateView.as_view(), name='cours-update'),
    path('supprimer/<int:pk>/', CoursDeleteView.as_view(), name='cours-delete'),
    path('imprimer/', imprimer_cours_pdf, name='imprimer-pdf'),
]