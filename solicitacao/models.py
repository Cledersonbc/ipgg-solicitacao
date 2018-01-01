from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Modelo da Solicitação
class ModelSolicitacao(models.Model):
    unidade = models.CharField('Unidade', max_length=100)
    gerencia = models.CharField('Gerência', max_length=60)
    setor = models.CharField('Setor', max_length=60)
    solicitante = models.CharField('Solicitante', max_length=60)
    data = models.DateField('Data', default=timezone.now)
    TIPO_EVENTO_CHOICES = (
        ('Curso', 'Curso'), ('Capacitação', 'Capacitação'), ('Treinamento', 'Treinamento'),
        ('Educação Continuada', 'Educação Continuada'), ('Congresso', 'Congresso'),
        ('Outros', 'Outros')
    )
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    outro_evento = models.CharField('Outro Evento', max_length=60, blank=True)
    justificativa = models.TextField('Justificativa', max_length=500)
    diagnostico = models.TextField('Diagnóstico Situacional', max_length=500)
    PRIORIDADE_CHOICES = (
        ('Alta', 'Alta'), ('Moderada', 'Moderada'), ('Baixa', 'Baixa')
    )
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES)
    REALIZACAO_CHOICES = (
        ('Setor', 'Setor'), ('Individual', 'Individual'),
        ('Categoria', 'Categoria'), ('Qual', 'Qual')
    )
    evento_realizado = models.CharField(max_length=10, choices=REALIZACAO_CHOICES)
    qual_evento = models.CharField('Qual Evento', max_length=60, blank=True)
    qtd_participante = models.IntegerField('Quantidade de Participantes', default=1)
    part_individual = models.TextField('Participação Individual', max_length=500, blank=True)
    PROJETO_CHOICES = (
        ('Educação Permanente em Saúde', 'Educação Permanente em Saúde'),
        ('Comunicação Corporativa', 'Comunicação Corporativa'),
        ('Relacionamento Interpessoal', 'Relacionamento Interpessoal'),
        ('Desenvolvimento e Acompanhamento de Projetos', 'Desenvolvimento e Acompanhamento de Projetos'),
        ('Qualidade de Vida', 'Qualidade de Vida'), ('Processos de Trabalho', 'Processos de Trabalho'),
        ('Treinamento em Informática e Sistemas de Informação','Treinamento em Informática e Sistemas de Informação'),
        ('Humanização', 'Humanização')
    )
    eixo_basico = models.CharField(max_length=55, choices=PROJETO_CHOICES)
    acao_nao_vinculada = models.TextField('Ação Não Vinculada', max_length=500, blank=True)
    impacto_esperado_instituicao = models.TextField('Impacto Institucional', max_length=500)
    impacto_esperado_setor = models.TextField('Impacto no Setor', max_length=500)
    mensuracao = models.TextField('Mensuração dos Dados', max_length=500)
    status = models.CharField('Status', max_length=20, blank=True, default='em avaliação')

    def __str__(self):
        return str(self.id) + ' - ' + self.tipo_evento


# Modelo da Avaliação GRH e GEG da solicitação
class ModelAvaliacao(models.Model):
    solicitacao_n = models.OneToOneField(ModelSolicitacao, on_delete=models.CASCADE)
    responsavel = models.CharField('Responsável', max_length=30)
    COMPLEX_CHOICES = (
        ('Alta', 'Alta'), ('Média', 'Média'), ('Baixa', 'Baixa')
    )
    complexidade = models.CharField(max_length=10, choices=COMPLEX_CHOICES)

    RECURSOS_CHOICES = (
        ('Próprio', 'Próprio'), ('Outros', 'Outros')
    )
    recursos = models.CharField(max_length=100, choices=RECURSOS_CHOICES)
    outro_recurso = models.CharField('Outro Recurso', max_length=60, blank=True)
    estimativa = models.IntegerField('Estimativa para a ação?', default=1)
    VIABILIDADE_CHOICES = (
        ('Sim', 'Sim'), ('Não', 'Não')
    )
    viabilidade = models.CharField(max_length=5, choices=VIABILIDADE_CHOICES)
    data_prev = models.DateField('Data Prevista', default=timezone.now, blank=True)

    def __str__(self):
        return 'Avaliação ' + str(self.id)


# Modelo do Usuário a ser registrado no sistema
class ModelUsuario(models.Model):
    nome_login = models.CharField('Usuário', max_length=30)
    primeiro_nome = models.CharField('Nome', max_length=30)
    ultimo_nome = models.CharField('Último Nome', max_length=30)
    setor = models.CharField('Setor', max_length=50, blank=True, default='')
    email = models.EmailField('Email', max_length=30)


# Modelo da Gerência
class ModelGerencia(models.Model):
    nome = models.CharField('Nome', max_length=30)
    descricao = models.CharField('Descricao', max_length=200)


# Modelo dos Setores que pertencem a uma gerência
class ModelSetor(models.Model):
    nome = models.CharField('Nome', max_length=30)
    descricao = models.CharField('Descricao', max_length=200)
    gerencia = models.ForeignKey(ModelGerencia, on_delete=models.CASCADE)


# Informações adicionais sobre o perfil do usuário registrado no sistema, como setor e gerência
class ModelPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    setor = models.OneToOneField(ModelSetor, on_delete=models.CASCADE)


