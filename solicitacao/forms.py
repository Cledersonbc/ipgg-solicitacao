from django import forms
from django.forms import ModelForm
from .models import *


# Formulário da solicitação
class FormSolicitacao(ModelForm):
    class Meta:
        model = ModelSolicitacao

        fields = [
            'unidade', 'gerencia', 'setor',
            'solicitante', 'data',
            'tipo_evento', 'outro_evento',
            'justificativa', 'diagnostico',
            'prioridade', 'evento_realizado',
            'qual_evento', 'qtd_participante',
            'part_individual', 'eixo_basico',
            'acao_nao_vinculada',
            'impacto_esperado_instituicao',
            'impacto_esperado_setor', 'mensuracao'
        ]


# Formulário da Avaliação
class FormAvaliacao(ModelForm):
    class Meta:
        model = ModelAvaliacao

        fields = [
            'solicitacao_n', 'responsavel',
            'complexidade', 'recursos', 'outro_recurso',
            'estimativa', 'viabilidade', 'data_prev'
        ]


# Formulário Setor
class FormSetor(ModelForm):
    class Meta:
        model = ModelSetor

        fields = ['nome', 'descricao', 'gerencia']


# Formulário Gerência
class FormGerencia(ModelForm):
    class Meta:
        model = ModelGerencia

        fields = ['nome', 'descricao']


# Formulário do Usuário (cadastro)
class FormUsuario(ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())
    conf_senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = ModelUsuario

        fields = [
            'nome_login',
            'primeiro_nome',
            'ultimo_nome',
            'senha', 'conf_senha',
            'email', 'setor'
        ]