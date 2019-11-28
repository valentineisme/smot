from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, logout, login as authlogin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import relacao, objeto, restricao, casos, comunidade, imagem, usuario, historico, User
from .forms import UsuarioForm, ComunidadeForm, ImagemForm, CasoForm, BuscarCasoForm
from datetime import datetime, timedelta


# inicios
def index(request):
    form = UsuarioForm()
    ComunidadeList = comunidade.objects.all()
    paginator = Paginator(ComunidadeList, 7)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'form': form, 'dados': dados})

def login(request):
    form = UsuarioForm()
    ComunidadeList = comunidade.objects.all()
    paginator = Paginator(ComunidadeList, 7)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)
    return render(request, 'blocos/erroLogar.html', {'form': form, 'dados': dados})


# usuario
def CadUser(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
    return render(request, 'index.html', {'form': form})


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

                return index(request)
    return login(request)


# comunidade
@login_required
def Comunidade(request):
    current_user = usuario.objects.get(email=request.user)
    ComunidadeList = comunidade.objects.filter(id_usuario=current_user)
    ComunidadeOutros = comunidade.objects.filter(permissao='S').exclude(id_usuario=current_user)
    if request.GET.get('pages'):
        ativo = 2
    else:
        ativo = 1

    form = ComunidadeForm()
    paginator = Paginator(ComunidadeList, 7)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)

    paginator = Paginator(ComunidadeOutros, 7)
    page = request.GET.get('pages')
    try:
        dadosOutros = paginator.page(page)
    except PageNotAnInteger:
        dadosOutros = paginator.page(1)
    except EmptyPage:
        dadosOutros = paginator.page(paginator.num_pages)
    return render(request, 'comunidade/comunidade.html', {"ativo": ativo, "outros":dadosOutros, "dados": dados, "form": form})


@login_required
def Comunidade_Cadastro(request):
    if request.POST:
        form = ComunidadeForm(request.POST)
        current_user = usuario.objects.get(email=request.user)
        if form.is_valid():
            comu = comunidade()
            comu.nome = request.POST['nome']
            comu.bairro = request.POST['bairro']
            comu.cidade = request.POST['cidade']
            comu.estado = request.POST['estado']
            comu.id_usuario = current_user
            # post = form.save(commit=False)
            # post.id_usuario = current_user
            # post.id_usuario = request.user.id
            comu.save()
            id_comunidade = comu.id
            print(id_comunidade)
            if request.POST.get('monitorar'):
                return HttpResponseRedirect('/monitoramento/' + str(id_comunidade))
            else:
                return redirect('Comunidade')
        else:
            print(form.errors)
            return render(request, 'comunidade/comunidade.html', {'form': form, 'method': 'post'})
    else:
        return index(request)


@login_required
def Comunidade_Edit(request):
    if request.POST['comu_id']:
        comu_id = request.POST['comu_id']
        comu = comunidade.objects.get(pk=comu_id)
        form = ComunidadeForm(request.POST)
        if form.is_valid():
            comu.nome = request.POST['nome']
            comu.bairro = request.POST['bairro']
            comu.cidade = request.POST['cidade']
            comu.estado = request.POST['estado']
            comu.save()
        return redirect('Comunidade')


@login_required
def Comunidade_Edit_Campos(request):
    if request.GET['comu']:
        comu_id = request.GET['comu']
        comu = comunidade.objects.filter(id=comu_id)
        json = serializers.serialize("json", comu)
        return HttpResponse(json)


@login_required
def Comunidade_Excluir(request, comu_id=None, page=None):
    comu = comunidade.objects.get(pk=comu_id)
    if comu.id != None:
        comu.delete()
    return redirect('/Comunidade/?page=' + page)

@login_required
def Comunidade_Permitir(request, comu_id=None, page=None):
    comu = comunidade.objects.get(pk=comu_id)
    current_user = usuario.objects.get(email=request.user)
    if comu.id != None:
        if comu.permissao == "S":
            comu.permissao = "N"
            imgs = imagem.objects.filter(comunidade = comu, usuario=current_user)
            for im in imgs:
                im.permissao = "N"
                im.save()
        elif comu.permissao == "N":
            comu.permissao = "S"
        comu.save()
    return redirect('/Comunidade/?page=' + page)

@login_required
def Comunidade_Utilizar(request, comu_id=None):
    comu = comunidade.objects.get(pk = comu_id)
    current_user = usuario.objects.get(email=request.user)
    if comu.id != None:
        c = comunidade()
        c.nome = comu.nome
        c.estado = comu.estado
        c.cidade = comu.cidade
        c.bairro = comu.bairro
        c.id_usuario = current_user
        c.save()
    return redirect('Comunidade')


# imagem
@login_required
def Imagem(request, id_comunidade=None):
    form = ImagemForm()
    current_user = usuario.objects.get(email=request.user)
    comunidades = comunidade.objects.filter(id_usuario=current_user)
    ComunidadeOutros = comunidade.objects.filter(permissao='S').exclude(id_usuario=current_user)
    # imagem = imagem.objects.filter()
    return render(request, 'imagem/imagem.html', {'form': form, 'comunidades': comunidades, 'comu_outros': ComunidadeOutros})

@login_required
def Imagem_Publica(request, comu_id=None):
    current_user = usuario.objects.get(email=request.user)
    if request.POST.get('comu'):
        comu = comunidade.objects.get(id=request.POST.get('comu'))
        return render(request, 'imagem/imagem_pub.html',
                      {'comu': comu})
    if request.GET.get('dataImagem'):
        dataImagem = request.GET.get('dataImagem')
        comu = request.GET.get('comu')
        current_comu = comunidade.objects.get(pk = comu)
        img = imagem.objects.filter(dataImagem=dataImagem, permissao='S', comunidade = current_comu)
        if img != None:
            json = serializers.serialize("json", img)
            return HttpResponse(json)
        else:
            return redirect('Imagem_Publica')
    if request.GET.get('img'):
        pkimagem = request.GET.get('img')
        img = imagem.objects.filter(pk=pkimagem, permissao='S')
        if img != None:
            json = serializers.serialize("json", img)
            return HttpResponse(json)
        # imagens = imagem.objects.filter(dataImagem=request.GET.get('data_imagem'))
        # imagens = imagem.objects.filter(comunidade = comu)
        # return render(request, 'imagem/imagem_pub.html',
        #               {'comuna': comu, 'dataImagem': dataImagem})


@login_required
def Imagem_Lista(request, comu_id=None):
    form = ImagemForm()
    comunidades = comunidade.objects.all()
    current_user = usuario.objects.get(email=request.user)
    if request.POST.get('comu'):
        curent_comunidade = comunidade.objects.get(id=request.POST.get('comu'))
    elif request.GET.get('comu'):
        curent_comunidade = comunidade.objects.get(id=request.GET.get('comu'))
    else:
        curent_comunidade = comunidade.objects.get(id=comu_id)

    ImagemList = imagem.objects.filter(comunidade=curent_comunidade, usuario=current_user).order_by('dataImagem')
    paginator = Paginator(ImagemList, 3)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)
    return render(request, 'imagem/listaImagens.html',
                  {'form': form, 'comunidades': comunidades, 'comunidade': curent_comunidade, 'dados': dados})


@login_required
def Imagem_Cadastro(request):
    form = ImagemForm()
    current_user = usuario.objects.get(email=request.user)
    if request.POST:
        im = imagem()
        im.dataImagem = request.POST['data']
        im.comunidade = comunidade.objects.get(id=request.POST['comu'])
        im.latitude = request.POST['lati']
        im.longitude = request.POST['longi']
        im.img = request.FILES['img']
        im.usuario = current_user
        im.save()
        if request.POST.get('monitorar'):
            return HttpResponseRedirect('/monitoramento/?idcomu=' + str(im.comunidade.id) + '&idimagem=' + str(im.id))
        else:
            return HttpResponseRedirect('/Imagem_Lista/' + str(im.comunidade.id) + '/')

    return render(request, 'imagem/cadastro_imagem.html', {'file': request.FILES})


@login_required
def Imagem_Excluir(request, img_id=None, comu_id=None, page=None):
    im = imagem.objects.get(pk=img_id)
    if im.id != None:
        im.delete()
    return redirect('/Imagem_Lista/' + comu_id + '/?page=' + page)

@login_required
def Imagem_Permitir(request, comu_id = None, img_id=None, page=None):
    img = imagem.objects.get(pk=img_id)
    comu = comunidade.objects.get(pk=img.comunidade.pk)
    if img.id != None:
        if img.permissao == "S":
            img.permissao = "N"
        elif img.permissao == "N":
            img.permissao = "S"
            if img.comunidade.permissao == "N":
                comu.permissao = "S"
                comu.save()
        img.save()
        comu_id = int(img.comunidade.id)
    return redirect('/Imagem_Lista/' + str(comu_id) + '/?page=' + page)

@login_required
def Imagem_Edit(request):
    if request.POST['img_id']:
        img_id = request.POST['img_id']
        img = imagem.objects.get(pk=img_id)
        if img.id != None:
            img.dataImagem = request.POST['data']
            img.latitude = request.POST['lati']
            img.longitude = request.POST['longi']
            img.save()
        return redirect('/Imagem_Lista/' + str(img.comunidade.id) + '/')


@login_required
def Imagem_Edit_Campos(request):
    if request.GET['img']:
        img_id = request.GET['img']
        img = imagem.objects.filter(id=img_id)
        json = serializers.serialize("json", img)
        return HttpResponse(json)

@login_required
def Imagem_Utilizar(request, img_id=None):
    img = imagem.objects.get(pk = img_id)
    current_user = usuario.objects.get(email=request.user)
    if img.id != None:
        c = comunidade()
        i = imagem()
        c.nome = img.comunidade.nome
        c.estado = img.comunidade.estado
        c.cidade = img.comunidade.cidade
        c.bairro = img.comunidade.bairro
        c.id_usuario = current_user
        c.save()
        i.comunidade = c
        i.latitude = img.latitude
        i.longitude = img.longitude
        i.img = img.img
        i.dataImagem = img.dataImagem
        i.usuario = current_user
        i.save()
    return redirect('Comunidade')

# caso
@login_required
def Casos(request, caso_id = None):
    form = CasoForm()
    current_user = usuario.objects.get(email = request.user)
    if request.POST.get('objeto1') or request.GET.get('ob1') or caso_id:
        if request.GET:
            objeto1 = request.GET.get('ob1')
            relac = request.GET.get('rel')
            objeto2 = request.GET.get('ob2')
        elif caso_id:
            current_caso = casos.objects.get(id = caso_id)
            objeto1 = current_caso.objeto1.id
            relac = current_caso.relacao.id
            objeto2 = current_caso.objeto2.id
        elif request.POST:
            form = CasoForm(request.POST)
            objeto1 = request.POST.get('objeto1')
            relac = request.POST.get('relacao')
            objeto2 = request.POST.get('objeto2')

        ob1 = objeto.objects.get(id=objeto1)
        rela = relacao.objects.get(id=relac)
        ob2 = objeto.objects.get(id=objeto2)

        rel = ob1.nome+" "+rela.nome+" "+ob2.nome
        current_casos = casos.objects.filter(objeto1=objeto1, relacao=relac, objeto2 = objeto2, id_usuario=current_user)
        current_casos1 = casos.objects.filter(objeto1=objeto2, relacao=relac, objeto2 = objeto1, id_usuario=current_user)

        if current_casos:
            current_casos1 = current_casos | current_casos1

        paginator = Paginator(current_casos1, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)
        return render(request, 'caso/casoLista.html', {'form':form, 'dados': dados, 'rel':rel, 'ob1':ob1.id,'rela':rela.id,'ob2':ob2.id})
    return render(request, 'caso/caso.html', {'form': form})

@login_required
def Casos_Excluir(request, caso_id=None, ob1_id = None, rel_id=None, ob2_id = None):
    c = casos.objects.get(id = caso_id)
    if c.id != None:
        c.delete()
    return redirect('/Casos/?ob1='+str(ob1_id)+'&rel='+str(rel_id)+'&ob2='+str(ob2_id)+'&deletado')


@login_required
def CadCaso(request):
    if request.POST:
        form = CasoForm(request.POST)
        # print(form.id_usuario_id)
        if form.is_valid():
            post = form.save(commit=False)
            current_user = usuario.objects.get(email=request.user)
            post.id_usuario = current_user
            post.save()
            if request.POST.get('monitorar'):
                return resultadoCaso(request)
            return redirect('/Casos/?ob1='+str(post.objeto1.id)+'&rel='+str(post.relacao.id)+'&ob2='+str(post.objeto2.id))
        else:
            print(form.errors)
        return redirect('/Casos/')

@login_required
def Caso_Edit_Campos(request):
    if request.GET['caso']:
        caso_id = request.GET['caso']
        c = casos.objects.filter(id=caso_id)
        form = CasoForm(c)
        json = serializers.serialize("json", c)
        return HttpResponse(json)

@login_required
def Caso_Edit(request):
    if request.POST['caso_id']:
        caso_id = request.POST['caso_id']
        c = casos.objects.get(pk=caso_id)
        if c:
            c.distancia = request.POST['distancia']
            c.resultado = request.POST['resultado']
            c.plano_acao = request.POST['plano_acao']
            c.save()
        return redirect('/Casos/' + str(c.id) + '/')

@login_required
def resultadoCaso(request):
    if request.POST:
        form = BuscarCasoForm(request.POST)
        id_imagem = request.POST.get("caso_inserido")
        current_imagem = imagem.objects.get(id=id_imagem)
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
    step = 4
    form = CasoForm(request.POST)
    antigo = []
    similar = []
    o1 = []
    relac = []
    o2 = []
    metros = []
    novo = ''
    plano = []
    monitorando = True
    cor = []
    current_user = usuario.objects.get(email=request.user)
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

        if (int(novoProblema[3]) >= caso[7]):
            percent_caso_novo = 100
        else:
            percent_caso_novo = (int(novoProblema[3]) * 100) / caso[7]

        if (caso[3] >= caso[7]):
            percent_caso_velho = 100
        else:
            percent_caso_velho = (caso[3] * 100) / caso[7]
        distancia_percent = percent_caso_novo - percent_caso_velho
        distancia_percent = abs(distancia_percent)

        if (0 <= distancia_percent <= 25):
            simi_dist = 0
        elif (26 <= distancia_percent <= 50):
            simi_dist = 13
        elif (51 <= distancia_percent <= 75):
            simi_dist = 26
        else:
            simi_dist = 40

        if distancia == 0.0:
            simi = 100
        elif distancia == 0.4:
            simi = 75
        elif distancia == 0.8:
            simi = 50
        else:
            simi = 0

        simi = simi - simi_dist
        resultado = [caso, novoProblema, distancia, simi]
        if (resultado[2] == 0.0 or resultado[2] == 0.4 or resultado[2] == 0.8):
            return resultado

    if request.POST.get('filtro_caso') == "geral":
        casolist = casos.objects.order_by('-id')
    else:
        casolist = casos.objects.filter(id_usuario=current_user).order_by('-id')
    for caso in casolist:
        velhoCaso = [str(caso.objeto1), str(caso.relacao), str(caso.objeto2), caso.distancia, str(caso.resultado),
                     str(caso.plano_acao), caso.id, caso.restricao.distancia]
        velhoCaso1 = [str(caso.objeto2), str(caso.relacao), str(caso.objeto1), caso.distancia, str(caso.resultado),
                      str(caso.plano_acao), caso.id, caso.restricao.distancia]
        current = distancia(peso, velhoCaso, novoCaso)
        current1 = distancia(peso, velhoCaso1, novoCaso)
        if type(current) == list:
            resultado.append(current)
        if type(current1) == list:
            resultado.append(current1)
    resultado.sort(key=lambda x: x[3], reverse = True)
    for r in resultado:
        antigo.append(r[0])
        o1.append(r[0][0])
        relac.append(r[0][1])
        o2.append(r[0][2])
        metros.append(r[0][3])
        plano.append(r[0][5])
        cor.append(r[0][4])
        similar.append(r[3])
        novo = r[1][0] + " " + r[1][1] + " " + r[1][2] + " a " + r[1][3] + " metros"
    # paginator = Paginator(resultado, 3)
    # page = request.GET.get('page')
    # try:
    #     dados = paginator.page(page)
    # except PageNotAnInteger:
    #     dados = paginator.page(1)
    # except EmptyPage:
    #     dados = paginator.page(paginator.num_pages)
    casolist_test = casos.objects.filter(id_usuario=current_user).order_by('-id')
    for c in casolist_test:
        restricao = c.restricao.descricao
        restricao_id = c.restricao.id
    return render(request, 'monitoramento/monitoramento_casos_similares.html',
                  {"rest": restricao, "rest_id": restricao_id, "monitorando":monitorando, "novo": novo, "metros": metros, "cor": cor, "plano": plano, "o1": o1, "relac": relac, "o2": o2,
                   "step": step, "resultado":resultado, "id_comu": current_imagem.comunidade.id, "current_imagem":current_imagem, "id_imagem": id_imagem, 'form': form, 'antigo': antigo,
                   'similaridade': similar})


# monitoramento
@login_required
def monitoramento(request, id_comunidade=None):
    current_user = usuario.objects.get(email=request.user)
    comunidades = comunidade.objects.all()
    form = ComunidadeForm()
    monitorando = True
    if request.POST.get("comu"):
        step = 2
        form = ImagemForm()
        comunidade_selecionada = request.POST.get("comu")
        c = comunidade.objects.get(id=comunidade_selecionada)
        im = imagem.objects.filter(comunidade=c, usuario=current_user).order_by('dataImagem')
        paginator = Paginator(im, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)
        monitorando = True
        return render(request, 'monitoramento/monitoramento_imagem.html',
                      {'monitorando':monitorando, 'step': step, 'comunidades': comunidades, 'comunidade': c,
                       'id_comunidade': comunidade_selecionada, 'dados': dados, 'form':form})
    elif id_comunidade:
        step = 2
        c = comunidade.objects.get(id=id_comunidade)
        im = imagem.objects.filter(comunidade=c, usuario=current_user).order_by('dataImagem')
        form = ImagemForm()

        paginator = Paginator(im, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)

        monitorando = True
        return render(request, 'monitoramento/monitoramento_imagem.html',
                      {'monitorando':monitorando, 'step': step, 'comunidades': comunidades, 'comunidade': c, 'id_comunidade': id_comunidade,
                       'dados': dados, 'form':form})
    elif request.POST.get("imagem_selecionada") or (request.GET.get("idcomu") and request.GET.get("idimagem")):
        step = 3
        if request.POST.get("imagem_selecionada"):
            id_comu = request.POST.get("comunidade")
            im = imagem.objects.get(id=request.POST.get("imagem_selecionada"))
        elif request.GET.get("idcomu") and request.GET.get("idimagem"):
            id_comu = request.GET.get("idcomu")
            im = imagem.objects.get(id=request.GET.get("idimagem"))
        form = BuscarCasoForm()
        return render(request, 'monitoramento/monitoramento_caso.html',
                      {'step': step, 'form': form, 'imagem': im, 'comunidade': id_comu})
    elif request.POST.get("caso_inserido") or request.GET.get("resultado"):
        return resultadoCaso(request)
    elif request.POST.get("caso_selecionado"):
        return cadHistorico(request)
    else:
        ComunidadeList = comunidade.objects.filter(id_usuario=current_user)
        step = 1
        return render(request, 'monitoramento/monitoramento_comu.html', {'form':form, 'monitorando':monitorando, 'step': step, 'comunidades': ComunidadeList})


# historico
@login_required
def cadHistorico(request):
    result = []
    step = 5
    antigo = ''
    novo = ''
    simi = ''
    if request.POST:
        resultado_selecionado = request.POST.get('resultado')
        id_imagem = request.POST.get('caso_selecionado')
    elif request.caso_selecionado:
        resultado_selecionado = request.resultado
        id_imagem = request.caso_selecionado
    result = resultado_selecionado.split("],")
    for letra in result[0]:
        if letra in "[]' ":
            pass
        else:
            antigo += letra

    for letra in result[1]:
        if letra in "[]' ":
            pass
        else:
            novo += letra

    for letra in result[2]:
        if letra in "[]' ":
            pass
        else:
            simi += letra
    antigoList = antigo.split(",")
    novoList = novo.split(",")
    simiList = simi.split(",")

    if novoList[1] == "Pertode":
        novoList[1] = "Perto de"
    elif novoList[1] == "Dentrode":
        novoList[1] = "Dentro de"

    current_caso = casos.objects.get(id=antigoList[6])
    current_restricao = restricao.objects.get(descricao=current_caso.restricao)
    current_imagem = imagem.objects.get(id=int(id_imagem))
    DistRestricao = current_restricao.distancia
    current_ob1 = objeto.objects.get(nome=novoList[0])
    current_rel = relacao.objects.get(nome=novoList[1])
    current_ob2 = objeto.objects.get(nome=novoList[2])

    DistNovo = novoList[3]
    now = datetime.now()

    current_user = usuario.objects.get(email=request.user)

    h = historico(usuario=current_user, imagem=current_imagem, dataImagem=current_imagem.dataImagem, lati=current_imagem.latitude, longe=current_imagem.longitude, data=now, objeto1=novoList[0], relacao=novoList[1],
                  objeto2=novoList[2], distancia=DistNovo, resultado=antigoList[4], plano_acao=antigoList[5])
    h.save()

    c = casos( objeto1=current_ob1, relacao=current_rel, objeto2=current_ob2, id_usuario=current_user, distancia=DistNovo, restricao=current_restricao,
               resultado=antigoList[4], plano_acao=antigoList[5], permissao='S')

    c.save()

    relacionamentoAntigo = antigoList[0] + " " + antigoList[1] + " " + antigoList[2]
    relacionamentoNovo = novoList[0] + " " + novoList[1] + " " + novoList[2]
    # novos = novoList[0] + " " + novoList[1] + " " + novoList[2] + " a " + novoList[3] + " metros"
    distancia_antiga = antigoList[3]
    resultado = antigoList[4]
    plano_acao = antigoList[5]
    return render(request, 'monitoramento/monitoramento_final.html',
                  {'resultado':resultado, 'plano':plano_acao, 'relAntigo':relacionamentoAntigo,'relNovo':relacionamentoNovo,'current_imagem':current_imagem, "id_imagem":current_imagem.id, "id_comu":current_imagem.comunidade.id, "antigo": antigo, "novo": novo, "simi": simiList[1], "restricao": DistRestricao, "dist_antiga":distancia_antiga, "distancia": DistNovo,
                   "step": step})


@login_required
def Historico(request):
    current_user = usuario.objects.get(email=request.user)
    ComunidadeList = comunidade.objects.filter(id_usuario = current_user)
    lists_imagens = []

    if request.POST.get('comu') or request.GET.get('comu'):
        if request.POST.get('comu'):
            current_comu = comunidade.objects.get(id=request.POST.get('comu'))
        elif request.GET.get('comu'):
            current_comu = comunidade.objects.get(id=request.GET.get('comu'))
        imagemList = imagem.objects.filter(comunidade=current_comu, usuario=current_user).order_by('dataImagem')
        for imlist in imagemList:
            valor_hist = 0
            list_validate = {}
            hist_list = historico.objects.all()
            for h in hist_list:
                if h.imagem.id == imlist.id:
                    valor_hist = 1
                    break

            list_validate['id'] = imlist.id
            list_validate['img'] = imlist.img
            list_validate['usuario'] = imlist.usuario
            list_validate['dataImagem'] = imlist.dataImagem
            list_validate['latitude'] = imlist.latitude
            list_validate['longitude'] = imlist.longitude
            list_validate['comunidade'] = imlist.comunidade
            list_validate['permissao'] = imlist.permissao
            list_validate['hist'] = valor_hist
            lists_imagens.append(list_validate)
        paginator = Paginator(lists_imagens, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)

        botao = 'historico_imagens'
        return render(request, 'historico/historico_imagem.html', {"list_validate": list_validate, "dados": dados, "comunidade": current_comu, "voltar_hist":botao})
    elif request.POST.get("imagem_selecionada") or (request.GET.get("id_comu") and request.GET.get("id_imagem")):
        if request.POST.get("imagem_selecionada"):
            current_comu = comunidade.objects.get(id=request.POST.get('comunidade'))
            current_imagem = imagem.objects.get(id=request.POST.get("imagem_selecionada"))
        elif (request.GET.get("id_comu") and request.GET.get("id_imagem")):
            current_comu = comunidade.objects.get(id=request.GET.get('id_comu'))
            current_imagem = imagem.objects.get(id=request.GET.get("id_imagem"))
        historicoList = historico.objects.filter(imagem=current_imagem, usuario=current_user).order_by('dataImagem')

        paginator = Paginator(historicoList, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)



        return render(request, 'historico/historico_final.html',
                      {"imagem": current_imagem, "dados": dados, 'comunidade': current_comu})
    elif request.POST.get("imagem_selecionada_lati") or request.GET.get("lati"):
        if request.POST.get("imagem_selecionada_lati"):
            current_comu = comunidade.objects.get(id=request.POST.get('comunidade'))
            current_imagem = imagem.objects.get(id=request.POST.get("imagem_selecionada_lati"))
        elif (request.GET.get("id_comu_lati") and request.GET.get("id_imagem_lati")):
            current_comu = comunidade.objects.get(id=request.GET.get('id_comu_lati'))
            current_imagem = imagem.objects.get(id=request.GET.get("id_imagem_lati"))
        historicoList = historico.objects.filter(longe=current_imagem.longitude, lati=current_imagem.latitude, usuario=current_user).order_by('dataImagem')

        paginator = Paginator(historicoList, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)

        return render(request, 'historico/historico_final.html',
                      {"imagem": current_imagem, "dados": dados, 'comunidade': current_comu, 'lati': current_imagem.latitude, 'longe': current_imagem.longitude})
    else:
        return render(request, 'historico/historico_comu.html', {"comunidades": ComunidadeList})

@login_required
def Historico_Excluir(request, hist_id=None, imagem_id=None, comu_id=None, page=None):
    h = historico.objects.get(pk=hist_id)
    if h.id != None:
        h.delete()
    return redirect('/Historico/?page=' + page + '&id_comu=' + str(comu_id) + '&id_imagem=' + str(imagem_id))

@login_required()
def Historico_Excluir_Lati(request, hist_id=None, imagem_id=None, comu_id=None, page=None):
    h = historico.objects.get(pk=hist_id)
    if h.id != None:
        h.delete()
    return redirect('/Historico/?page=' + page + '&id_comu_lati=' + str(comu_id) + '&id_imagem_lati=' + str(imagem_id) + '&lati=0')

@login_required
def ComparacaoHist(request):
    if request.POST:
        historico = request.POST.get('historico')
    # histList = historico.split(",")
    # hist = histList[6].strip("]")

    return render(request, 'ComparacaoHist.html', {"historico": historico})


@login_required
def sair(request):
    logout(request)
    return index(request)
