from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from .models import Cours
from .forms import CoursForm
from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm


class AccueilView(TemplateView):
    template_name = 'cours/accueil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cours'] = Cours.objects.count()
        context['total_enseignants'] = Cours.objects.values('enseignant').distinct().count()
        context['dernier_cours'] = Cours.objects.order_by('-date_ajout').first()
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cours/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cours'] = Cours.objects.count()
        context['total_enseignants'] = Cours.objects.values('enseignant').distinct().count()
        context['dernier_cours'] = Cours.objects.order_by('-date_ajout').first()
        context['cours_recents'] = Cours.objects.order_by('-date_ajout')[:5]
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


def imprimer_cours_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_cours.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    titre_style = ParagraphStyle(
        'titre', parent=styles['Title'],
        fontSize=20, textColor=colors.HexColor('#1a3c6e'), spaceAfter=10
    )
    elements.append(Paragraph("Liste des Cours", titre_style))
    date_str = timezone.now().strftime("%d/%m/%Y à %H:%M")
    sous_titre_style = ParagraphStyle(
        'sous_titre', parent=styles['Normal'],
        fontSize=10, textColor=colors.grey, spaceAfter=20
    )
    elements.append(Paragraph(f"Imprimé le {date_str}", sous_titre_style))
    elements.append(Spacer(1, 0.5*cm))
    cours_list = Cours.objects.all().order_by('-date_ajout')
    data = [['N°', 'Titre du cours', 'Enseignant', 'Date de publication']]
    for i, cours in enumerate(cours_list, 1):
        data.append([
            str(i),
            cours.titre,
            cours.enseignant,
            cours.date_publication.strftime("%d/%m/%Y")
        ])
    table = Table(data, colWidths=[1.5*cm, 7*cm, 6*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3c6e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4fa')]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ddd')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1a3c6e')),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'footer', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey, alignment=1
    )
    elements.append(Paragraph(
        f"Total : {cours_list.count()} cours | GestionCours © {timezone.now().year}",
        footer_style
    ))
    doc.build(elements)
    return response