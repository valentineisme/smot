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


    url(r'^Imagem/$', views.Imagem, name='Imagem'),
    url(r'^Imagem_Lista/$', views.Imagem_Lista, name='Imagem_Lista'),
    url(r'^Imagem_Lista/(?P<comu_id>\d+)/$', views.Imagem_Lista, name='Imagem_Lista'),
    url(r'^Imagem_Lista/Delete/(?P<img_id>\d+)/(?P<comu_id>\d+)/$', views.Imagem_Excluir, name='Imagem_Excluir'),
    # url(r'^Imagem/(?P<id_comunidade>\d+)/$', views.Imagem, name='Imagem'),
    url(r'^Imagem_Cadastro/$', views.Imagem_Cadastro, name='Imagem_Cadastro'),

    url(r'^FormCaso/', views.FormCaso, name='FormCaso'),
    url(r'^CadCaso/', views.CadCaso, name='CadCaso'),
    url(r'^BuscarCaso/$', views.BuscarCaso, name='BuscarCaso'),
    url(r'^BuscarCaso/(?P<id_imagem>\d+)/$', views.BuscarCaso, name='BuscarCaso'),
    url(r'^resultadoCaso/', views.resultadoCaso, name='resultadoCaso'),

    url(r'^cadHistorico/', views.cadHistorico, name='cadHistorico'),
    url(r'^Historico/$', views.Historico, name='Historico'),
    url(r'^Historico/Delete/(?P<hist_id>\d+)/(?P<imagem_id>\d+)/(?P<comu_id>\d+)/$', views.Historico_Excluir, name='Historico_Excluir'),
    url(r'^ComparacaoHist/', views.ComparacaoHist, name='ComparacaoHist'),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
