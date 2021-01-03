from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

""" 
Extension of the User Creation Form to add address fields.
"""


class SignUpForm(UserCreationForm):
    #fields for address
    address_line_1 = forms.CharField(max_length=50, required=True)
    address_line_2 = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=10, required=True)
    country = forms.CharField(max_length=15, required=True)
    zip_code = forms.CharField(max_length=8, required=True)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address_line_1', 'address_line_2',
                  'city', 'country', 'zip_code', 'birth_date', 'password1', 'password2')


""" 
Form for submitting of reviews for purchases made.
"""


class ReviewForm(forms.Form):
    item_rating = forms.DecimalField(
        min_value=0, max_value=5, required=True)  # item rating 0 - 5
    review_text = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea()
    )  # text field for review details
