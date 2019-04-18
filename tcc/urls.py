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
    url(r'^inicial/', views.inicial, name='inicial'),
    url(r'^CadUser/$', views.CadUser, name='CadUser'),
    url(r'^validacao/$', views.validacao, name='validacao'),
    url(r'^sair/$', views.sair, name='sair'),
    #url(r'^area/$', views.caso_area, name='area'),
    url(r'^FormComunidade/$', views.FormComunidade, name='FormComunidade'),
    url(r'^CadComunidade/$', views.CadComunidade, name='CadComunidade'),
    url(r'^FormImagem/$', views.FormImagem, name='FormImagem'),
    url(r'^FormImagem/(?P<id_comunidade>\d+)/$', views.FormImagem, name='FormImagem'),
    url(r'^CadImagem/$', views.CadImagem, name='CadImagem'),
    url(r'^FormCaso/', views.FormCaso, name='FormCaso'),
    url(r'^CadCaso/', views.CadCaso, name='CadCaso'),
    url(r'^BuscarCaso/$', views.BuscarCaso, name='BuscarCaso'),
    url(r'^BuscarCaso/(?P<id_imagem>\d+)/$', views.BuscarCaso, name='BuscarCaso'),
    url(r'^resultadoCaso/', views.resultadoCaso, name='resultadoCaso'),
    url(r'^cadHistorico/', views.cadHistorico, name='cadHistorico'),
    url(r'^MostrarHistoricos/', views.MostrarHistoricos, name='MostrarHistoricos'),
    url(r'^ComparacaoHist/', views.ComparacaoHist, name='ComparacaoHist'),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
