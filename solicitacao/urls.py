from django.conf.urls import url
from . import views

app_name = 'solicitacao'

urlpatterns = [
    # /solicitacao
    url(r'^$', views.index, name='index'),

    # /solicitacao/login
    url(r'^login/$', views.login_usuario, name='login_usuario'),

    # /solicitacao/logout
    url(r'^logout/$', views.logout_usuario, name='logout_usuario'),

    # /solicitacao/signup
    url(r'^signup/$', views.signup, name='signup'),

    # /solicitacao/perfil
    url(r'^perfil/$', views.perfil, name='perfil'),

    # solicitacao/cadastro
    url(r'^cadastro/$', views.cadastro, name='cadastro'),

    # solicitacao/lista-solicitacoes
    url(r'^lista-solicitacoes/$', views.lista_solicitacoes, name='lista_solicitacoes'),

    # solicitacao/lista-solicitacoes/del-solicitacao
    url(r'^lista-solicitacoes/del-solicitacao/(?P<solicitacao_id>[0-9]+)/$', views.del_solicitacao, name='del_solicitacao'),

    # solicitacao/avaliar
    url(r'^avaliar/(?P<solicitacao_id>[0-9]+)/$', views.avaliar, name='avaliar'),

    # solicitacao/lista-avaliacoes
    url(r'^lista-avaliacoes/$', views.lista_avaliacoes, name='lista_avaliacoes'),

    # solicitacao/lista-solicitacoes/del-avaliacao
    url(r'^lista-avaliacoes/del-avaliacao/(?P<avaliacao_id>[0-9]+)/$', views.del_avaliacao, name='del_avaliacao'),

    # solicitacao/avaliacao/visualizar
    url(r'^avaliacao/visualizar/(?P<avaliacao_id>[0-9]+)/$', views.avaliacao_visualizar, name='avaliacao_visualizar'),

    # solicitacao/visualizar
    url(r'^visualizar/(?P<solicitacao_id>[0-9]+)/$', views.visualizar, name='visualizar'),
]