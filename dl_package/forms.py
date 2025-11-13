from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import verPost, zipFile, Profile, serialNumber

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
        fields = ('upload',)

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username','email')

class serialNumberForm(forms.Form):
    serial_number = forms.CharField(
        max_length=8,
        label='シリアル番号',
        widget=forms.TextInput(attrs={'placeholder': '8桁のシリアル番号を入力'})
    )

    def clean_serial_number(self):
        serial = self.cleaned_data.get('serial_number')

        if not serial.isdigit() or len(serial) != 8:
            raise forms.ValidationError('8桁の数字を入力してください')
        return serial