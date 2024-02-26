
from django import forms
from .models import Expenses
from bootstrap_datepicker_plus.widgets import DatePickerInput
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator

class ExpensesForm(forms.ModelForm):
    date = forms.DateField(widget=DatePickerInput(attrs={'class': 'form-control rounded'}))
    choice = forms.ChoiceField(choices=Expenses.Choice.choices, widget=forms.Select(attrs={'class': 'form-control rounded'}))
    
    deposit = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control rounded'}))

    class Meta:
        model = Expenses
        fields = ['date', 'choice', 'deposit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values from model instance
        if not self.instance.pk:  # Check if the instance is not saved (new form)
            self.fields['date'].initial = Expenses._meta.get_field('date').get_default()
            self.fields['choice'].initial = Expenses._meta.get_field('choice').get_default()
            self.fields['deposit'].initial = Expenses._meta.get_field('deposit').get_default()


class SignupForm(UserCreationForm):
    username = forms.CharField(validators=[RegexValidator(r'^[a-zA-Z0-9_.]+$', 'Enter a valid username with alphanumeric characters, underscores, or dots')])
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[MinLengthValidator(8, 'Password must be at least 8 characters long')])
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, validators=[MinLengthValidator(8, 'Password must be at least 8 characters long')])

    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username=cleaned_data['username']).exists():
            raise ValidationError("Username already exists.")
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError("Passwords do not match.")
        # Add password strength validation here using libraries like zxcvbn or django-password-validators
        # ...
        return cleaned_data



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))