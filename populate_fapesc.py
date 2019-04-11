import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcc.settings')

import django
django.setup()

from fapesc.models import relacao, restricao, objeto, casos, usuario


def populate():
    # add_usuario(nome="admin",
    #             sobrenome="admin",
    #             dataNasc="1980-01-01",
    #             rua="Rua",
    #             numero=68,
    #             bairro="bairro",
    #             cidade="cidade",
    #             estado="estado",
    #             email="email@gmail.com",
    #             senha="senha",
    #             formacao="formacao",)

    add_objeto(nome="Floresta",)
    add_objeto(nome="Reflorestamento",)
    add_objeto(nome="Campo",)
    add_objeto(nome="Terras Aridas",)
    add_objeto(nome="Recursos Hidricos (Doce)",)
    add_objeto(nome="Recursos Hidricos (Salobra)",)
    add_objeto(nome="Cultivo",)
    add_objeto(nome="Mineracao",)
    add_objeto(nome="Construcao",)
    add_objeto(nome="Ferrovia",)
    add_objeto(nome="Rodovia",)

    add_relacao(nome="Perto de",)
    add_relacao(nome="Toca",)
    add_relacao(nome="Sobrepoe",)
    add_relacao(nome="Igual",)
    add_relacao(nome="Dentro de",)
    add_relacao(nome="Contem",)

    add_restricao(descricao="Res01: Art20. Faixas Rodoviarias: 200m, ambos os lados", distancia=200,)
    add_restricao(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos", distancia=200,)
    add_restricao(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas", distancia=500,)
    add_restricao(descricao="Res04: de 10 (dez) metros, para rios de largura inferior a 20 (vinte) metros", distancia=10,)
    add_restricao(descricao="Res05: Lagoas e Lagos: 100m", distancia=100,)
    add_restricao(descricao="Res06: Nascentes: 50m", distancia=50,)

    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Floresta")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=600,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Floresta")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=400,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Floresta")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Floresta")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Reflorestamento")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=600,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Reflorestamento")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=400,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Reflorestamento")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Reflorestamento")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Terras Aridas")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=600,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Terras Aridas")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=400,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Terras Aridas")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Terras Aridas")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Cultivo")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=600,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Cultivo")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=400,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Cultivo")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Cultivo")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res03: Art44. 500m de largura em torno de parques estaduais, estacoes ecologicas e reservas biologicas")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Doce)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=300,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Doce)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=400,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Doce)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Doce)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Salobra)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=300,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Verde",
              plano_acao="Okay",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Perto de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Salobra)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=100,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Toca")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Salobra)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Amarelo",
              plano_acao="Recuar",)
    add_casos(objeto1=objeto.objects.get_or_create(nome="Construcao")[0],
              relacao=relacao.objects.get_or_create(nome="Dentro de")[0],
              objeto2=objeto.objects.get_or_create(nome="Recursos Hidricos (Salobra)")[0],
              id_usuario=usuario.objects.get_or_create(nome="Noah")[0],
              distancia=0,
              restricao=restricao.objects.get_or_create(descricao="Res02: Art9. Construcoes que causam riscos devem ficar 200m dos recursos hidricos")[0],
              resultado="Vermelho",
              plano_acao="Retirar",)


# def add_usuario(nome, sobrenome, dataNasc, rua, numero, bairro, cidade, estado, email, senha, formacao):
#     u = usuario.objects.get_or_create(nome=nome, sobrenome=sobrenome, dataNasc=dataNasc, rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, email=email, senha=senha, formacao=formacao)[0]
#     u.save()
#     return u

def add_objeto(nome):
    o = objeto.objects.get_or_create(nome=nome)[0]
    o.save()
    return o

def add_relacao(nome):
    r= relacao.objects.get_or_create(nome=nome)[0]
    r.save()
    return r

def add_restricao(descricao, distancia=0):
    res = restricao.objects.get_or_create(descricao = descricao, distancia = distancia)[0]
    res.save()
    return res

def add_casos(objeto1, relacao, objeto2, id_usuario, distancia, restricao, resultado, plano_acao):
    c = casos.objects.get_or_create(objeto1=objeto1, relacao=relacao, objeto2=objeto2, id_usuario=id_usuario, distancia=distancia, restricao=restricao, resultado=resultado, plano_acao=plano_acao)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print ("Starting Rango population script...")
    populate()
