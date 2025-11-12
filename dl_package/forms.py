from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import verPost, zipFile, Profile

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

class serialNumberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['serial_number']

    def clean_serial_number(self):
        serial = self.cleaned_data.get('serial_number')
        if not serial.isdigit() or len(serial) != 8:
            raise forms.ValidationError('8桁のシリアル番号を入力してください')
        return serial