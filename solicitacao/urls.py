from django.conf.urls import url
from . import views

app_name = 'solicitacao'

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),

    # /login
    url(r'^login/$', views.login_usuario, name='login_usuario'),

    # /logout
    url(r'^logout/$', views.logout_usuario, name='logout_usuario'),

    # /signup
    url(r'^signup/$', views.signup, name='signup'),

    # /perfil
    url(r'^perfil/$', views.perfil, name='perfil'),

    # /cadastro
    url(r'^cadastro/$', views.cadastro, name='cadastro'),

    # /lista-solicitacoes
    url(r'^lista-solicitacoes/$', views.lista_solicitacoes, name='lista_solicitacoes'),

    # /lista-solicitacoes/del-solicitacao
    url(r'^lista-solicitacoes/del-solicitacao/(?P<solicitacao_id>[0-9]+)/$', views.del_solicitacao, name='del_solicitacao'),

    # /solicitacao/avaliar
    url(r'^solicitacao/avaliar/(?P<solicitacao_id>[0-9]+)/$', views.avaliar, name='avaliar'),

    # /lista-avaliacoes
    url(r'^lista-avaliacoes/$', views.lista_avaliacoes, name='lista_avaliacoes'),

    # /lista-solicitacoes/del-avaliacao
    url(r'^lista-avaliacoes/del-avaliacao/(?P<avaliacao_id>[0-9]+)/$', views.del_avaliacao, name='del_avaliacao'),

    # /avaliacao/visualizar
    url(r'^avaliacao/visualizar/(?P<avaliacao_id>[0-9]+)/$', views.avaliacao_visualizar, name='avaliacao_visualizar'),

    # /solicitacao/visualizar
    url(r'^solicitacao/visualizar/(?P<solicitacao_id>[0-9]+)/$', views.visualizar, name='visualizar'),
]
