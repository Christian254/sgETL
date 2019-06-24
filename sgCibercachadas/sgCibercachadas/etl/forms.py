from django import forms
from django.core.validators import FileExtensionValidator

class RetornoForm(forms.Form):
    file_retorno=forms.FileField(validators=[FileExtensionValidator(['xlsx'])])

class PotencialForm(forms.Form):
    file_potencial=forms.FileField(validators=[FileExtensionValidator(['xlsx'])])
    
class ConsignaForm(forms.Form):
    file_consigna=forms.FileField(validators=[FileExtensionValidator(['xlsx'])])



