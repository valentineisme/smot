from django import forms
import datetime
from .models import usuario, imagem, comunidade, casos

class UsuarioForm(forms.ModelForm):

    nome = forms.CharField(max_length=78, help_text='Nome:')
    sobrenome = forms.CharField(max_length=128, help_text='Sobrenome:')
    dataNasc = forms.DateField(help_text='Data:')

    rua = forms.CharField(max_length=128, help_text='Rua:')
    numero = forms.IntegerField(help_text='Numero:')
    bairro = forms.CharField(max_length=128, help_text='Bairro:')
    cidade = forms.CharField(max_length=128, help_text='Cidade:')
    estado = forms.CharField(max_length=128, help_text='Estado:')
    email = forms.CharField(max_length=128, help_text='E-mail:')
    senha = forms.CharField(max_length=128, widget=forms.PasswordInput, help_text='Senha:')

    class Meta:
        model = usuario
        fields = ('nome','sobrenome','dataNasc','rua','numero','bairro','cidade','estado','email','senha')


class ComunidadeForm(forms.ModelForm):
    nome = forms.CharField(max_length=78, help_text='Nome:')
    bairro = forms.CharField(max_length=128, help_text='Bairro:')
    cidade = forms.CharField(max_length=128, help_text='Cidade:')
    estado = forms.CharField(max_length=128, help_text='Estado:')
    class Meta:
        model = comunidade
        fields = '__all__'

class ImagemForm(forms.ModelForm):
    img = forms.ImageField()
    dataImagem = forms.DateField(widget=forms.TextInput(attrs={'onfocus': 'limita_data_final()'}))
    latitude = forms.CharField(max_length=78, help_text='Latitude:')
    longitude = forms.CharField(max_length=78, help_text='Longitude:')

    class Meta:
        model = imagem
        fields = '__all__'

class CasoForm(forms.ModelForm):

    class Meta:
        model = casos
        fields = '__all__'
        exclude = ('id_usuario',)

class BuscarCasoForm(forms.ModelForm):

    class Meta:
        model = casos
        fields = '__all__'
        exclude = ('id_usuario', 'restricao', 'resultado', 'plano_acao')