from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import verPost, zipFile

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

class zipUploadForm(forms.ModelForm):
    class Meta:
        model = zipFile
        fields = ('description', 'upload',)

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username','email')