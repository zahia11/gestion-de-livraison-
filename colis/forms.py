from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from .models import Profile
from .models import Colis
from django import forms
from django.forms.widgets import PasswordInput, TextInput 
#create user 



class CreateUserForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        validators=[RegexValidator(regex='^[0-9]*$', message='Only numeric values are allowed.')]
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.save()  # Save the user instance first
            phone_number = self.data.get('phone_number')
            Profile.objects.update_or_create(user=user, defaults={'phone_number': phone_number})
        return user

      

#login user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

#creation de colis 
class CreateColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields = ['nom_produits', 'nom_destinataire', 'adr_destinataire', 'region', 'num_destinataire', 'prix']
       

class UpdateColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields = ['user', 'code', 'nom_produits', 'nom_destinataire', 'adr_destinataire', 'region', 'num_destinataire', 'prix'] 

class UpdateProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=8,
        required=True,
        validators=[RegexValidator(regex='^[0-9]*$', message='Only numeric values are allowed.')],
        widget=forms.NumberInput()  
    )
    new_password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(),
        help_text="Laissez vide si vous ne souhaitez pas changer votre mot de passe."
    )
    confirm_password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(),
        help_text="Confirmez votre nouveau mot de passe."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'new_password', 'confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Vérifier et changer le mot de passe si un nouveau mot de passe est fourni
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password:  # Vérifiez si le nouveau mot de passe est fourni
            if new_password != confirm_password:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
            user.set_password(new_password)  # Crypter le mot de passe

        if commit:
            user.save()
            phone_number = self.cleaned_data.get('phone_number')
            Profile.objects.update_or_create(user=user, defaults={'phone_number': phone_number})

        return user