from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class UsuarioForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"name":"username" ,
    "class":"form-control ","placeholder":"Escriba Username","autocomplete":"off",}))
    nombres=forms.CharField(widget=forms.TextInput(attrs={"name":"nombres" ,
    "class":"form-control ","placeholder":"Escriba sus nombres","autocomplete":"off"},))
    apellidos=forms.CharField(widget=forms.TextInput(attrs={"name":"apellidos" ,
    "class":"form-control ","placeholder":"Escriba sus apellidos","autocomplete":"off"},))
    email=forms.CharField(widget=forms.TextInput(attrs={"name":"email" ,
    "class":"form-control ","placeholder":"Escriba su email","type":"email","autocomplete":"off"},))
    password=forms.CharField(widget=forms.TextInput(attrs={"name":"password" ,
    "class":"form-control ","placeholder":"Escriba su contraseña","type":"password","autocomplete":"off"},))
    password2=forms.CharField(widget=forms.TextInput(attrs={"name":"password2" ,
    "class":"form-control ","placeholder":"Escriba su contraseña","type":"password","autocomplete":"off"},))
    
    def AddIsInvalid(self):
        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' is-invalid'
        print(self.fields)

    def clean(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password!=password2:
            self.add_error('password',"Las contraseñas no coinciden")
        if len(password)< 8 :
            self.add_error('password',"La contraseña debe ser mayor que 8 caracter")
        if not (any(x.isupper() for x in password) and any(x.islower() for x in password)  and any(x.isdigit() for x in password)):
            self.add_error('password',"La contraseña debe al menos una letra en mayuscula, una letra en minuscula, un digito")
        return password
