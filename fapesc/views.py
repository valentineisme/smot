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
    form = ComunidadeForm()
    paginator = Paginator(ComunidadeList, 2)
    page = request.GET.get('page')
    try:
        dados = paginator.page(page)
    except PageNotAnInteger:
        dados = paginator.page(1)
    except EmptyPage:
        dados = paginator.page(paginator.num_pages)

    paginator = Paginator(ComunidadeOutros, 2)
    page = request.GET.get('page')
    try:
        dadosOutros = paginator.page(page)
    except PageNotAnInteger:
        dadosOutros = paginator.page(1)
    except EmptyPage:
        dadosOutros = paginator.page(paginator.num_pages)
    return render(request, 'comunidade/comunidade.html', {"outros":dadosOutros, "dados": dados, "form": form})


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
def Comunidade_Excluir(request, comu_id=None):
    comu = comunidade.objects.get(pk=comu_id)
    if comu.id != None:
        comu.delete()
    return redirect('Comunidade')

@login_required
def Comunidade_Permitir(request, comu_id=None):
    comu = comunidade.objects.get(pk=comu_id)
    if comu.id != None:
        if comu.permissao == "S":
            comu.permissao = "N"
        elif comu.permissao == "N":
            comu.permissao = "S"
        comu.save()
    return redirect('Comunidade')

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
        im.img = request.POST['imagem']
        im.usuario = current_user
        im.save()
        if request.POST.get('monitorar'):
            return redirect('/monitoramento/?idcomu=' + str(im.comunidade.id) + '&idimagem=' + str(im.id))
        else:
            return redirect('/Imagem_Lista/' + str(im.comunidade.id) + '/')

    return render(request, 'imagem/cadastro_imagem.html', {'form': form, 'method': 'post'})


@login_required
def Imagem_Excluir(request, img_id=None, comu_id=None):
    im = imagem.objects.get(pk=img_id)
    if im.id != None:
        im.delete()
    return redirect('/Imagem_Lista/' + comu_id + '/')

@login_required
def Imagem_Permitir(request, comu_id = None, img_id=None):
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
    return redirect('/Imagem_Lista/' + str(comu_id) + '/')

@login_required
def Imagem_Edit(request):
    if request.POST['img_id']:
        img_id = request.POST['img_id']
        img = imagem.objects.get(pk=img_id)
        if img.id != None:
            img.dataImagem = request.POST['imagemData']
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

# caso
@login_required
def Casos(request):
    form = CasoForm()
    if request.POST.get('objeto1') or request.GET:
        if request.GET:
            objeto1 = request.GET.get('ob1')
            relac = request.GET.get('rel')
            objeto2 = request.GET.get('ob2')
        elif request.POST:
            form = CasoForm(request.POST)
            objeto1 = request.POST.get('objeto1')
            relac = request.POST.get('relacao')
            objeto2 = request.POST.get('objeto2')

        ob1 = objeto.objects.get(id=objeto1)
        rela = relacao.objects.get(id=relac)
        ob2 = objeto.objects.get(id=objeto2)

        rel = ob1.nome+" "+rela.nome+" "+ob2.nome
        current_casos = casos.objects.filter(objeto1=objeto1, relacao=relac, objeto2 = objeto2)
        current_casos1 = casos.objects.filter(objeto1=objeto2, relacao=relac, objeto2 = objeto1)

        if current_casos:
            current_casos1 = current_casos

        paginator = Paginator(current_casos1, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)
        return render(request, 'caso/casoLista.html', {'form':form, 'dados': dados, 'rel':rel})
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
            print(current_user.id)
            post.id_usuario = current_user

            post.save()
            if request.POST.get('monitorar'):
                return resultadoCaso(request)
            return Casos(request)
        else:
            print(form.errors)
        return redirect('/Casos/')

@login_required
def Caso_Edit_Campos(request):
    if request.GET['caso']:
        caso_id = request.GET['caso']
        c = casos.objects.filter(id=caso_id)
        json = serializers.serialize("json", c)
        return HttpResponse(json)

@login_required
def Caso_Edit(request):
    if request.POST['caso_id']:
        caso_id = request.POST['caso_id']
        c = casos.objects.get(pk=caso_id)
        ob1 = objeto.objects.get(pk=request.POST['objeto1'])
        rel = relacao.objects.get(pk=request.POST['relacao'])
        ob2 = objeto.objects.get(pk=request.POST['objeto2'])
        rest = restricao.objects.get(pk=request.POST['restricao'])
        form = CasoForm(request.POST)
        if form.is_valid():
            c.objeto1 = ob1
            c.relacao = rel
            c.objeto2 = ob2
            c.distancia = request.POST['distancia']
            c.restricao = rest
            c.resultado = request.POST['resultado']
            c.plano_acao = request.POST['plano_acao']
            c.save()
        return Casos(request)

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
    cor = []
    monitoramento = True

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
            simi = "nenhum caso similares"
        resultado = [caso, novoProblema, distancia, simi]
        if (resultado[2] == 0.0 or resultado[2] == 0.4):  # or resultado[2] == 0.8):
            return resultado

    casolist = casos.objects.order_by('-id')
    for caso in casolist:
        velhoCaso = [str(caso.objeto1), str(caso.relacao), str(caso.objeto2), caso.distancia, str(caso.resultado),
                     str(caso.plano_acao), caso.id]
        velhoCaso1 = [str(caso.objeto2), str(caso.relacao), str(caso.objeto1), caso.distancia, str(caso.resultado),
                      str(caso.plano_acao), caso.id]
        current = distancia(peso, velhoCaso, novoCaso)
        current1 = distancia(peso, velhoCaso1, novoCaso)
        if type(current) == list:
            resultado.append(current)
        if type(current1) == list:
            resultado.append(current1)
    resultado.sort(key=lambda x: x[2])
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

    # paginator = Paginator(casolist, 3)
    # page = request.GET.get('page')
    # try:
    #     dados = paginator.page(page)
    # except PageNotAnInteger:
    #     dados = paginator.page(1)
    # except EmptyPage:
    #     dados = paginator.page(paginator.num_pages)
    return render(request, 'monitoramento/monitoramento_casos_similares.html',
                  {"monitorando":monitoramento, "novo": novo, "metros": metros, "cor": cor, "plano": plano, "o1": o1, "relac": relac, "o2": o2,
                   "step": step, "resultado": resultado, "id_comu": current_imagem.comunidade.id, "current_imagem":current_imagem, "id_imagem": id_imagem, 'form': form, 'antigo': antigo,
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
                       'id_comunidade': comunidade_selecionada, 'dados': dados})
    elif id_comunidade:
        step = 2
        c = comunidade.objects.get(id=id_comunidade)
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
                      {'monitorando':monitorando, 'step': step, 'comunidades': comunidades, 'comunidade': c, 'id_comunidade': id_comunidade,
                       'dados': dados})
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
    elif request.POST.get("caso_inserido") or request.GET.get("similar"):
        return resultadoCaso(request)
    elif request.POST.get("caso_selecionado"):
        return cadHistorico(request)
    else:
        ComunidadeList = comunidade.objects.all()
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
    result = resultado_selecionado.split("],")
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
    simiList = simi.split(",")

    current_caso = casos.objects.get(id=antigoList[6])
    current_restricao = restricao.objects.get(descricao=current_caso.restricao)
    current_imagem = imagem.objects.get(id=int(id_imagem))
    DistRestricao = current_restricao.distancia

    DistNovo = novoList[3]
    now = datetime.now()

    current_user = usuario.objects.get(email=request.user)

    h = historico(usuario=current_user, imagem=current_imagem, data=now, objeto1=novoList[0], relacao=novoList[1],
                  objeto2=novoList[2], distancia=DistNovo, resultado=antigoList[4], plano_acao=antigoList[5])
    h.save()

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
    ComunidadeList = comunidade.objects.all()
    if request.POST.get('comu') or request.GET.get('comu'):
        if request.POST.get('comu'):
            current_comu = comunidade.objects.get(id=request.POST.get('comu'))
        elif request.GET.get('comu'):
            current_comu = comunidade.objects.get(id=request.GET.get('comu'))
        imagemList = imagem.objects.filter(comunidade=current_comu, usuario=current_user).order_by('dataImagem')
        paginator = Paginator(imagemList, 3)
        page = request.GET.get('page')
        try:
            dados = paginator.page(page)
        except PageNotAnInteger:
            dados = paginator.page(1)
        except EmptyPage:
            dados = paginator.page(paginator.num_pages)

        botao = 'historico_imagens'
        return render(request, 'historico/historico_imagem.html', {"dados": dados, "comunidade": current_comu, "voltar_hist":botao})
    elif request.POST.get("imagem_selecionada") or (request.GET.get("id_comu") and request.GET.get("id_imagem")):
        if request.POST.get("imagem_selecionada"):
            current_comu = comunidade.objects.get(id=request.POST.get('comunidade'))
            current_imagem = imagem.objects.get(id=request.POST.get("imagem_selecionada"))
        elif (request.GET.get("id_comu") and request.GET.get("id_imagem")):
            current_comu = comunidade.objects.get(id=request.GET.get('id_comu'))
            current_imagem = imagem.objects.get(id=request.GET.get("id_imagem"))
        historicoList = historico.objects.filter(imagem=current_imagem, usuario=current_user)
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
    else:
        return render(request, 'historico/historico_comu.html', {"comunidades": ComunidadeList})

@login_required
def Historico_Excluir(request, hist_id=None, imagem_id=None, comu_id=None):
    h = historico.objects.get(pk=hist_id)
    if h.id != None:
        h.delete()
    return redirect('/Historico/?id_comu=' + str(comu_id) + '&id_imagem='+ str(imagem_id))

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
