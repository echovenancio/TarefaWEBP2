from django import forms
from django.contrib.auth.hashers import make_password
from . import models


class ChangePassword(forms.ModelForm):
    new_pass = forms.CharField(widget=forms.PasswordInput, label="Nova senha")
    conf_pass = forms.CharField(widget=forms.PasswordInput, label="Confirmação nova senha")
    
    class Meta:
        model = models.User
        fields = ('hash_senha',)
        widgets = {
            'hash_senha': forms.PasswordInput()
        }
    
    def is_valid(self) -> bool:
        user = super().save(commit=False)
        if user.hash_senha == self.cleaned_data['hash_senha']:
            return self.cleaned_data['new_pass'] ==  self.cleaned_data['conf_pass']
        else:
            return False

    def save(self, commit=False):
        user = super().save(commit=False)
        user.hash_senha = make_password(self.cleaned_data['new_pass'])
        user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['name', 'email', 'hash_senha', 'foto']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'hash_senha': forms.PasswordInput(),
            'foto': forms.FileInput(attrs={"accept": "image/user/*"})
        }

    def save(self, commit=False):
        user = super().save(commit=False)
        user.hash_senha = make_password(self.cleaned_data['hash_senha'])
        user.save()
        return user

class FormLogin(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('email', 'hash_senha')
        widgets = {
            'email': forms.EmailInput(),
            'hash_senha': forms.PasswordInput()
        }

class CursoForm(forms.ModelForm):
    class Meta:
        model = models.Curso
        fields = ['name', 'author', 'duration', 'price', 'foto']
        widgets = {
            'name': forms.TextInput(),
            'author': forms.TextInput(),
            'duration': forms.NumberInput(),
            'price': forms.NumberInput(),
            'foto': forms.FileInput(attrs={"accept": "image/*"})
        }

class FotoForm(forms.ModelForm):
    class Meta:
        model = models.Foto
        fields = ['nome', 'foto']

        widgets = {
            'foto': forms.FileInput(attrs={"accept": "image/*"})
        }
