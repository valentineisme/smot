from django import forms
import datetime
from .models import usuario, imagem, comunidade, casos

class UsuarioForm(forms.Form):
    nome = forms.CharField(max_length=78, help_text='Nome:')
    sobrenome = forms.CharField(max_length=128, help_text='Sobrenome:')
    dataNasc = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    email = forms.CharField(max_length=128, help_text='E-mail', widget=forms.TextInput(attrs={"required": True}))
    senha = forms.CharField(max_length=128, widget=forms.PasswordInput, help_text='Senha:')


class ComunidadeForm(forms.ModelForm):
    nome = forms.CharField(max_length=78, help_text='Nome:')
    bairro = forms.CharField(max_length=128, help_text='Bairro:')
    cidade = forms.CharField(max_length=128, help_text='Cidade:')
    estado = forms.CharField(max_length=128, help_text='Estado:')
    class Meta:
        model = comunidade
        fields = '__all__'
        exclude = ('id_usuario','permissao')

class ImagemForm(forms.ModelForm):
    img = forms.ImageField()
    dataImagem = forms.DateField(widget=forms.TextInput(attrs={'type':'date', 'onfocus': 'limita_data_final()'}))
    latitude = forms.CharField(max_length=78, help_text='Latitude:')
    longitude = forms.CharField(max_length=78, help_text='Longitude:')

    class Meta:
        model = imagem
        fields = '__all__'
        exclude = ('id_usuario','usuario', 'permissao', 'comunidade')

class CasoForm(forms.ModelForm):

    class Meta:
        model = casos
        fields = '__all__'
        exclude = ('id_usuario','permissao')


class BuscarCasoForm(forms.ModelForm):
    class Meta:
        model = casos
        fields = '__all__'
        exclude = ('id_usuario', 'restricao', 'resultado', 'plano_acao', 'permissao')
        widgets = {
            'field_one': forms.TextInput(attrs={'id': 'objeto1'}),
            'field_two': forms.TextInput(attrs={'id': 'relacao'}),
            'field_three': forms.TextInput(attrs={'id': 'objeto2'}),
            'field_four': forms.TextInput(attrs={'id': 'distancia'})
        }

class BuscarCaso(forms.ModelForm):
    class Meta:
        model = casos
        fields = '__all__'
        exclude = ('id_usuario', 'restricao', 'resultado', 'plano_acao', 'distancia')
        widgets = {
            'field_one': forms.TextInput(attrs={'id': 'objeto1'}),
            'field_two': forms.TextInput(attrs={'id': 'relacao'}),
            'field_three': forms.TextInput(attrs={'id': 'objeto2'}),
            'field_four': forms.TextInput(attrs={'id': 'distancia'})
        }