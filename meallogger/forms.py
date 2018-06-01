from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from meallogger.models import Meal


class MealForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['mealtime'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Mealtime'})
        self.fields['item'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Item'})
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Quantity'})
        self.fields['unit'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Unit'})

    class Meta:
        model = Meal
        fields = ['mealtime', 'item', 'quantity', 'unit']


class CustomAuthForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})


class CustomSignUpForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm'})
