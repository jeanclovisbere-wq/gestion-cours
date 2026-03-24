from django import forms
from django.utils import timezone
from .models import Cours

class CoursForm(forms.ModelForm):
    date_publication = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'max': timezone.now().date,
                'class': 'date-input'
            }
        )
    )

    class Meta:
        model = Cours
        fields = ['titre', 'enseignant', 'date_publication']