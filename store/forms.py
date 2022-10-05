from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=200,required=True)
    telephone = forms.IntegerField(required=False,label='Teléfono')
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden',
    }
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Tu nombre',
        max_length=100, 
        help_text='Tu nombre',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Tu nombre',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'max_length' : 'Este nombre es demasiado largo',
        }
    )
    telephone = forms.IntegerField(
        help_text='2234556666',
        label='Tu teléfono',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Tu teléfono',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'invalid' : 'Por favor introducí un número válido',
        }
    )
    email = forms.EmailField(
        label='Tu email',
        max_length=100,
        help_text='Tu email',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Tu email',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'invalid' : 'Este email no es válido',
        }
    )
    comment = forms.CharField(
        label='Comentarios',
        max_length=1500,
        help_text='Comentarios',
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Tu consulta',
                'rows' : "4"
            }
        ),
        error_messages={
            'max_length' : 'Este comentario es demasiado largo'
        }
    )

    subject = forms.CharField(
        label='Tema del mensaje',
        max_length=200,
        help_text='Tema del mensaje',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Tema del mensaje',
            }
        ),
        error_messages={
            'max_length' : 'El texto es demasiado largo'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        self.name = cleaned_data.get('name')
        self.telephone = cleaned_data.get('telephone')
        self.email = cleaned_data.get('email')
        self.subject = cleaned_data.get('subject')
        self.comment = cleaned_data.get('comment')

    

class PedidoForm(forms.Form):
    name = forms.CharField(
        label='Tu nombre',
        max_length=100, 
        help_text='Tu nombre',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Magali Alliana',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'max_length' : 'Este nombre es demasiado largo',
        }
    )
    telephone = forms.IntegerField(
        help_text='2234556666',
        label='Tu teléfono',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : '2234556666',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'invalid' : 'Por favor introducí un número válido',
        }
    )
    email = forms.EmailField(
        label='Tu email',
        max_length=100,
        help_text='Tu email',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'tucorreo@email.com',
            }
        ),
        error_messages={
            'required' : 'Por favor completá este campo',
            'invalid' : 'Este email no es válido',
        }
    )
    comment = forms.CharField(
        label='Comentarios',
        max_length=1500,
        help_text='Comentarios',
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control form-control-lg',
                'placeholder' : 'Horario para contactar, preguntas sobre productos, etc.',
                'rows' : "4"
            }
        ),
        error_messages={
            'max_length' : 'Este comentario es demasiado largo'
        }
    )

    def clean(self):
        cleaned_data = super(PedidoForm, self).clean()
        self.name = cleaned_data.get('name')
        self.telephone = cleaned_data.get('telephone')
        self.email = cleaned_data.get('email')
        self.comment = cleaned_data.get('comment')