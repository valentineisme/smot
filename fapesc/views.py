from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, logout, login as authlogin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required
from .models import relacao, objeto, restricao, casos, comunidade, imagem, usuario, historico
from .forms import UsuarioForm, ComunidadeForm, ImagemForm, CasoForm, BuscarCasoForm
from datetime import datetime


def index(request):
    return render(request, 'index.html')
def inicial(request):
    return render(request, 'inicial.html')
def login(request):
    return render(request, 'login.html')

def CadUser(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.formacao = request.POST.get('formacao')
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = UsuarioForm()

    return render(request, 'CadUser.html', {'form': form})

def validacao(request):
    if request.user.id:
        return render(request, 'index.html')

    if request.POST:
        emailUser = request.POST.get('email')
        senhaUser = request.POST.get('senha')

        u = authenticate(username=emailUser, password=senhaUser)
        if u is not None:
            if u.is_active:
                authlogin(request, u)

                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return render(request, 'index.html')
    return login(request)



@login_required
def FormComunidade(request):
    form = ComunidadeForm()
    return render(request, 'FormComunidade.html', {'form': form})

@login_required
def CadComunidade(request):

    if request.POST:
        form = ComunidadeForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            id_comunidade = post.id
            print (id_comunidade)

            return HttpResponseRedirect('/FormImagem/'+str(id_comunidade))
            # print (id_comunidade)
            # return render_to_response('FormImagem.html',{'id_comunidade': id_comunidade},context_instance=RequestContext(request))
            # return render(request, self.template, {'form': form, 'method': 'get', 'id': id})
            # return render(request, 'FormImagem.html', {'form':form, 'method':'get', 'id_segurado': id_comunidade})
        else:
            print(form.errors)
        return render(request, 'FormComunidade.html', {'form': form, 'method': 'post'})
@login_required
def FormImagem(request, id_comunidade = None):
    if id_comunidade:
        id_comunidade = id_comunidade
    else:
        id_comunidade = None
    form = ImagemForm()
    form.comunidade = id_comunidade
    return render(request, 'FormImagem.html', {'form': form, 'id_comunidade': id_comunidade})

@login_required
def CadImagem(request):
    if request.POST:
        form = ImagemForm(request.POST, request.FILES)
        print (request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            id_imagem = post.id
            return HttpResponseRedirect('/BuscarCaso/'+str(id_imagem))
        else:
            print(form.errors)
        return render(request, 'FormImagem.html', {'form': form, 'method': 'post'})

@login_required
def FormCaso(request):
    form = CasoForm()
    return render(request, 'FormCaso.html', {'form': form})

@login_required
def CadCaso(request):
    if request.POST:
        form = CasoForm(request.POST)
        #print(form.id_usuario_id)
        if form.is_valid():
            post = form.save(commit=False)
            current_user = usuario.objects.get(email=request.user)
            print(current_user.id)
            post.id_usuario = current_user

            post.save()
            return render(request, 'index.html')
        else:
            print(form.errors)
        return render(request, 'FormCaso.html', {'form': form, 'method': 'post'})

@login_required
def BuscarCaso(request, id_imagem=None):
    if id_imagem:
        id_imagem = id_imagem
    else:
        id_imagem = 5
    form = BuscarCasoForm()
    form.id_imagem = id_imagem
    return render(request, 'BuscarCaso.html', {'form': form, 'id_imagem':id_imagem})

@login_required
def resultadoCaso(request):
    if request.POST:
        form = BuscarCasoForm(request.POST)
        id_imagem = request.POST.get("id_imagem")
        novoCaso = []
        for valor in form:
            if valor.name == "distancia":
                current_caso = int(valor.value())
            elif valor.name == "relacao":
                current_caso = relacao.objects.get(id=int(valor.value()))
            else:
                current_caso = objeto.objects.get(id=int(valor.value()))
            novoCaso.append(str(current_caso))
    peso = [0.8, 0.4, 0.8]
    resultado = []
    def EhIgual(x, y):
        if (x == y):
            peso = 0
        else:
            peso = 1
        return peso

    def distancia(peso, caso, novoProblema):
        pesoInstancias = []
        distancia = 0.0
        for i in range(0, len(peso)):
            pesoInstancias.append(EhIgual(str(caso[i]), novoProblema[i]))
        for i in range(0, len(peso)):
            distancia += (peso[i] * pesoInstancias[i])
        distancia = distancia
        if distancia == 0.0:
             simi = "100%"
        elif distancia == 0.4:
             simi = "75%"
        elif distancia == 0.8:
             simi = "50%"
        else:
            simi = "nenhum caso similar"
        resultado = [caso, novoProblema, distancia, simi]
        if (resultado[2] == 0.0 or resultado[2] == 0.4): # or resultado[2] == 0.8):
            return resultado

    casolist = casos.objects.order_by('-id')
    for caso in casolist:
        velhoCaso = [str(caso.objeto1), str(caso.relacao), str(caso.objeto2), caso.distancia, str(caso.resultado), str(caso.plano_acao), caso.id]
        velhoCaso1 = [str(caso.objeto2), str(caso.relacao), str(caso.objeto1), caso.distancia, str(caso.resultado), str(caso.plano_acao), caso.id]
        current = distancia(peso, velhoCaso, novoCaso)
        current1 = distancia(peso, velhoCaso1, novoCaso)
        if type(current) == list:
            resultado.append(current)
        if type(current1) == list:
            resultado.append(current1)
    resultado.sort(key=lambda x: x[2])
    return render(request, 'resultadoCaso.html', {"resultado":resultado, "id_imagem":id_imagem})

@login_required
def cadHistorico(request):
    result=[]
    antigo=''
    novo=''
    simi=''
    if request.POST:
        r = request.POST.get('resultado')
        id_imagem = request.POST.get('id_imagem')
    result = r.split("],")
    for letra in result[0]:
        if letra in "[]'":
            pass
        else:
            antigo += letra

    for letra in result[1]:
        if letra in "[]'":
            pass
        else:
            novo += letra

    for letra in result[2]:
        if letra in "[]'":
            pass
        else:
            simi += letra
    antigoList = antigo.split(",")
    novoList = novo.split(",")

    current_caso = casos.objects.get(id = antigoList[6])
    current_restricao = restricao.objects.get(descricao=current_caso.restricao)
    current_imagem = imagem.objects.get(id=int(id_imagem))
    DistRestricao = current_restricao.distancia

    DistNovo = novoList[3]
    now = datetime.now()
    current_user = usuario.objects.get(email=request.user)

    h = historico(usuario=current_user, imagem=current_imagem, data=now, objeto1=novoList[0], relacao=novoList[1], objeto2=novoList[2], distancia=DistNovo, resultado=antigoList[4], plano_acao=antigoList[5])
    h.save()

    return render(request, 'cadHistorico.html', {"antigo": antigo, "novo": novo, "simi":simi, "restricao":DistRestricao, "distancia":DistNovo})

@login_required
def MostrarHistoricos(request):
    current_user = usuario.objects.get(email = request.user)
    historicoList = historico.objects.filter(usuario = current_user)

    return render(request, 'MostrarHistoricos.html', {"historico": historicoList})

@login_required
def ComparacaoHist(request):
    if request.POST:
        historico = request.POST.get('historico')
    #histList = historico.split(",")
    #hist = histList[6].strip("]")


    return render(request, 'ComparacaoHist.html', {"historico": historico})

@login_required
def sair(request):
    logout(request)
    return index(request)