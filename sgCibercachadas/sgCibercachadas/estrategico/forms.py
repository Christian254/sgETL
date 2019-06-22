from django import forms
from collections import Counter
from datetime import datetime

class FechasForm(forms.Form):
    fechainicio=forms.CharField(widget=forms.TextInput(attrs={"name":"fechainicio" ,
    "class":"form-control col-6","placeholder":"Seleccione fecha","autocomplete":"off",}))
    fechafin=forms.CharField(widget=forms.TextInput(attrs={"name":"fechafin" ,
    "class":"form-control col-6","placeholder":"Seleccione fecha","autocomplete":"off"},))
    
    def AddIsInvalid(self):
            for field in self.errors:
                self[field].field.widget.attrs['class'] += ' is-invalid'
            print(self.fields)


    def clean_fechafin(self):
        
        fechafin = self.cleaned_data.get("fechafin")
        fechafin=datetime.strptime(fechafin,'%d/%m/%Y')

        if fechafin>datetime.today():
            raise forms.ValidationError("La fecha final es superior a la fecha de hoy")
        
        return fechafin


    def clean(self):
        cleaned_data = super().clean()

        fechainicio =cleaned_data.get("fechainicio")
        
        if fechainicio:
            fechainicio=datetime.strptime(fechainicio,'%d/%m/%Y')

        fechafin = self.cleaned_data.get("fechafin")

        #si no es none
        if fechafin and fechainicio:
            if fechafin<fechainicio:
                self.add_error('fechainicio',"La fecha inicial es mayor que la fecha final")
       


class CategoriaForm(FechasForm):
    categoria=forms.ChoiceField(choices=())

