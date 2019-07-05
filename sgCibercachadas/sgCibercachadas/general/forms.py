from django import forms

class PasswordForm(forms.Form):
    old_password=forms.CharField()
    new_password=forms.CharField()
    new_password_repeat=forms.CharField()
    
    def __init__(self, user, data=None):
        self.user = user
        super(PasswordForm, self).__init__(data=data)
    
    def clean_old_password(self):
        password=self.cleaned_data.get('old_password',None)
        if not self.user.check_password(password):
            raise forms.ValidationError("No es su contraseña!")
    
    def clean(self):
        password = self.cleaned_data.get('new_password')
        new_password_repeat = self.cleaned_data.get("new_password_repeat")

        if password!=new_password_repeat:
            self.add_error('new_password_repeat',"Las contraseñas no coinciden")
        if len(password)< 8 :
            self.add_error('new_password',"La contraseña debe ser mayor que 8 caracter")
        if not (any(x.isupper() for x in password) and any(x.islower() for x in password)  and any(x.isdigit() for x in password)):
            self.add_error('new_password',"La contraseña debe al menos una letra en mayuscula, una letra en minuscula, un digito")


    
