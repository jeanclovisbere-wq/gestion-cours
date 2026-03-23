from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cours

class CoursListView(ListView):
    model = Cours
    template_name = 'cours/liste_cours.html'
    context_object_name = 'cours_list'

class CoursCreateView(CreateView):
    model = Cours
    fields = ['titre', 'enseignant', 'date_publication']
    template_name = 'cours/cours_form.html'
    success_url = reverse_lazy('cours-list')
    extra_context = {'title': 'Ajouter un cours'}

class CoursUpdateView(UpdateView):
    model = Cours
    fields = ['titre', 'enseignant', 'date_publication']
    template_name = 'cours/cours_form.html'
    success_url = reverse_lazy('cours-list')
    extra_context = {'title': 'Modifier un cours'}

class CoursDeleteView(DeleteView):
    model = Cours
    template_name = 'cours/cours_confirm_delete.html'
    success_url = reverse_lazy('cours-list')