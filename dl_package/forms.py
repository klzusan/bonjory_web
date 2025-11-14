from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import verPost, zipFile, serialNumber, CustomUser

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
        model = CustomUser
        fields = ('email',) + UserCreationForm.Meta.fields[1:]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

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
    
class ContactForm(forms.Form):
    email = forms.EmailField(
        label = '*メールアドレス',
        widget = forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )

    name = forms.CharField(
        label='お名前',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'お名前'}),
        required=False
    )

    subject = forms.CharField(
        label = '*件名',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '件名'})
    )

    message = forms.CharField(
        label='*お問い合わせ内容',
        widget=forms.Textarea(attrs={'rows':5, 'placeholder': '具体的な内容をご記入ください'})
    )