from django import forms

from .models import verPost

class verPostForm(forms.ModelForm):

    class Meta:
        model = verPost
        fields = ('ver_num', 'ver_text', 'published_date')
        widgets = {
            'published_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
        }