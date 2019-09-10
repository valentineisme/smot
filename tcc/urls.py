from django.conf.urls import include, url
from django.contrib import admin
from fapesc import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'tcc_final.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^CadUser/$', views.CadUser, name='CadUser'),
    url(r'^validacao/$', views.validacao, name='validacao'),
    url(r'^sair/$', views.sair, name='sair'),

    #url(r'^area/$', views.caso_area, name='area'),
    url(r'^monitoramento/$', views.monitoramento, name='monitoramento'),
    url(r'^monitoramento/(?P<id_comunidade>\d+)/$', views.monitoramento, name='monitoramento'),

    url(r'^Comunidade/$', views.Comunidade, name='Comunidade'),
    url(r'^Comunidade_Cadastro/$', views.Comunidade_Cadastro, name='Comunidade_Cadastro'),
    url(r'^Comunidade/Edit/$', views.Comunidade_Edit, name='Comunidade_Edit'),
    url(r'^Comunidade/Edit_Campos/$', views.Comunidade_Edit_Campos, name='Comunidade_Edit_Campos'),
    url(r'^Comunidade/Delete/(?P<comu_id>\d+)/$', views.Comunidade_Excluir, name='Comunidade_Excluir'),
    url(r'^Comunidade/Permitir/(?P<comu_id>\d+)/$', views.Comunidade_Permitir, name='Comunidade_Permitir'),
    url(r'^Comunidade/Utilizar/(?P<comu_id>\d+)/$', views.Comunidade_Utilizar, name='Comunidade_Utilizar'),


    url(r'^Imagem/$', views.Imagem, name='Imagem'),
    url(r'^Imagem_Lista/$', views.Imagem_Lista, name='Imagem_Lista'),
    url(r'^Imagem_Lista/(?P<comu_id>\d+)/$', views.Imagem_Lista, name='Imagem_Lista'),
    url(r'^Imagem_Lista/(?P<comu_id>\d+)/Permitir/(?P<img_id>\d+)/$', views.Imagem_Permitir, name='Imagem_Permitir'),
    url(r'^Imagem_Lista/Delete/(?P<img_id>\d+)/(?P<comu_id>\d+)/$', views.Imagem_Excluir, name='Imagem_Excluir'),
    url(r'^Imagem_Lista/Permitir/(?P<img_id>\d+)/$', views.Imagem_Permitir, name='Imagem_Permitir'),
    url(r'^Imagem_Lista/Edit/$', views.Imagem_Edit, name='Imagem_Edit'),
    url(r'^Imagem_Lista/Edit_Campos/$', views.Imagem_Edit_Campos, name='Imagem_Edit_Campos'),
    url(r'^Imagem_Cadastro/$', views.Imagem_Cadastro, name='Imagem_Cadastro'),
    url(r'^Imagem_Publica/$', views.Imagem_Publica, name='Imagem_Publica'),
    url(r'^Imagem_Publica/Utilizar/(?P<img_id>\d+)/$', views.Imagem_Utilizar, name='Imagem_Utilizar'),

    url(r'^Casos/$', views.Casos, name='Casos'),
    url(r'^Casos/(?P<caso_id>\d+)/$', views.Casos, name='Casos'),
    url(r'^CadCaso/', views.CadCaso, name='CadCaso'),
    url(r'^Casos/Delete/(?P<caso_id>\d+)/(?P<ob1_id>\d+)/(?P<rel_id>\d+)/(?P<ob2_id>\d+)/$', views.Casos_Excluir, name='Casos_Excluir'),
    url(r'^Caso/Edit/$', views.Caso_Edit, name='Caso_Edit'),
    url(r'^Casos/Edit_Campos/$', views.Caso_Edit_Campos, name='Caso_Edit_Campos'),

    url(r'^cadHistorico/', views.cadHistorico, name='cadHistorico'),
    url(r'^Historico/$', views.Historico, name='Historico'),
    url(r'^Historico/Delete/(?P<hist_id>\d+)/(?P<imagem_id>\d+)/(?P<comu_id>\d+)/$', views.Historico_Excluir, name='Historico_Excluir'),
    url(r'^ComparacaoHist/', views.ComparacaoHist, name='ComparacaoHist'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
