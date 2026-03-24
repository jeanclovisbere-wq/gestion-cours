from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Cours
from .forms import CoursForm
from dateutil.relativedelta import relativedelta

class AccueilView(TemplateView):
    template_name = 'cours/accueil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cours'] = Cours.objects.count()
        context['total_enseignants'] = Cours.objects.values('enseignant').distinct().count()
        context['dernier_cours'] = Cours.objects.order_by('-date_publication').first()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cours/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cours'] = Cours.objects.count()
        context['total_enseignants'] = Cours.objects.values('enseignant').distinct().count()
        context['dernier_cours'] = Cours.objects.order_by('-date_publication').first()
        context['cours_recents'] = Cours.objects.order_by('-date_publication')[:5]
        cours_par_mois = []
        mois_labels = []
        for i in range(5, -1, -1):
            mois = timezone.now().date().replace(day=1)
            mois = mois - relativedelta(months=i)
            count = Cours.objects.filter(
                date_publication__year=mois.year,
                date_publication__month=mois.month
            ).count()
            cours_par_mois.append(count)
            mois_labels.append(mois.strftime('%b %Y'))
        context['cours_par_mois'] = cours_par_mois
        context['mois_labels'] = mois_labels
        return context

class CoursListView(ListView):
    model = Cours
    template_name = 'cours/liste_cours.html'
    context_object_name = 'cours_list'

    def get_queryset(self):
        queryset = Cours.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                titre__icontains=query
            ) | queryset.filter(
                enseignant__icontains=query
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class CoursCreateView(LoginRequiredMixin, CreateView):
    model = Cours
    form_class = CoursForm
    template_name = 'cours/cours_form.html'
    success_url = reverse_lazy('cours-list')
    login_url = '/login/'
    extra_context = {'title': 'Ajouter un cours'}

class CoursUpdateView(LoginRequiredMixin, UpdateView):
    model = Cours
    form_class = CoursForm
    template_name = 'cours/cours_form.html'
    success_url = reverse_lazy('cours-list')
    login_url = '/login/'
    extra_context = {'title': 'Modifier un cours'}

class CoursDeleteView(LoginRequiredMixin, DeleteView):
    model = Cours
    template_name = 'cours/cours_confirm_delete.html'
    success_url = reverse_lazy('cours-list')
    login_url = '/login/'