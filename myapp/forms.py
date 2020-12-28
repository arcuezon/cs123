from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    address_line_1 = forms.CharField(max_length=50, required=True)
    address_line_2 = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=15, required=True)
    zip_code = forms.CharField(max_length=8, required=True)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address_line_1','address_line_2',
        'city', 'country', 'zip_code', 'birth_date', 'password1', 'password2')