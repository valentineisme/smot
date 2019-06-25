from django.db import models
from django.contrib.auth.models import User


class relacao(models.Model):
    nome = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Relacao'
        verbose_name_plural = 'Relacoes'

    def __str__(self):
        return self.nome


class restricao(models.Model):
    descricao = models.CharField(max_length=128)
    distancia = models.IntegerField()

    class Meta:
        verbose_name = 'Restricao'
        verbose_name_plural = 'Restricoes'

    def __str__(self):
        return self.descricao


class objeto(models.Model):
    nome = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Objeto'
        verbose_name_plural = 'Objetos'

    def __str__(self):
        return self.nome


class usuario(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    nome = models.CharField(max_length=128)
    sobrenome = models.CharField(max_length=128)
    dataNasc = models.DateField(blank=True, null=True)
    # rua = models.CharField(max_length=128)
    # numero = models.IntegerField(default=0)
    # bairro = models.CharField(max_length=128)
    # cidade = models.CharField(max_length=128)
    # estado = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    senha = models.CharField(max_length=128, null=True)
    # formacao = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def save(self):
        if not self.id:
            c = usuario.objects.filter(email=self.email).count()
            if c:
                raise Exception("Email Existente")

            usr = User.objects.filter(username=self.email)
            if usr:
                u = usr[0]
            else:
                u = User.objects.create_user(self.email, self.email, self.senha)
            u.save()
            self.user = u
        else:
            self.user.username = self.email
            self.user.email = self.email
            self.user.set_password(self.senha)
            self.user.save()

        super(usuario, self).save()

    def __str__(self):
        return self.nome

class comunidade(models.Model):
    nome = models.CharField(max_length=128)
    bairro = models.CharField(max_length=128)
    cidade = models.CharField(max_length=128)
    estado = models.CharField(max_length=128)
    class Meta:
        verbose_name = 'Comunidade'
        verbose_name_plural = 'Comunidades'

    def __str__(self):
        return (self.nome)


class imagem(models.Model):
    img = models.ImageField(upload_to='static/media/media/', blank=True)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    dataImagem = models.DateField(blank=True)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)
    comunidade = models.ForeignKey(comunidade, on_delete=models.CASCADE)


    class Meta:
     verbose_name = 'Imagem'
     verbose_name_plural = 'Imagens'

    def __str__(self):
     return str(self.id)

class historico(models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    imagem = models.ForeignKey(imagem, null=True, on_delete=models.CASCADE)
    data = models.DateField(blank=True)
    objeto1 = models.CharField(max_length=128)
    relacao = models.CharField(max_length=128)
    objeto2 = models.CharField(max_length=128)
    distancia = models.IntegerField(default=0)
    resultado = models.CharField(max_length=128)
    plano_acao = models.CharField(max_length=128)


    class Meta:
     verbose_name = 'Historico'
     verbose_name_plural = 'Historico'

    def __str__(self):
     return self.plano_acao


class casos(models.Model):
    objeto1 = models.ForeignKey(objeto, related_name="objeto1", null=True, blank=False, on_delete=models.CASCADE)
    relacao = models.ForeignKey(relacao, blank=False, on_delete=models.CASCADE)
    objeto2 = models.ForeignKey(objeto, related_name="objeto2", null=True, blank=False, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    distancia = models.IntegerField(default=0)
    restricao = models.ForeignKey(restricao, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=128)
    plano_acao = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Caso'
        verbose_name_plural = 'Casos'

    def __str__(self):
        return (self.resultado)

# Create your models here.
