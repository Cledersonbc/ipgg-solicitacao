from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
import re


# Essa função valida se o usuário solicitante da requisição
# é um membro da equipe de avaliação ou não
def membro_avaliacao(request):
    autenticado = request.user.is_authenticated

    if autenticado:
        username = request.user.username
        usuario = User.objects.get(username__exact=username)
        membro = usuario.groups.filter(name='avaliador').exists()

        if not membro:
            return False
        else:
            return True

    else:
        return False


# Página inicial
def index(request):
    autenticado = request.user.is_authenticated

    if autenticado:
        username = request.user.username
        contexto = {'username': username, 'autenticado': autenticado}
        return render(request, 'solicitacao/index.html', contexto)
    else:
        return render(request, 'solicitacao/index.html')


# Autentificação de usuário
def login_usuario(request):

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        autenticado = authenticate(username=username, password=password)

        if autenticado is not None:
            login(request, autenticado)
            contexto = {'username': username, 'autenticado': autenticado}
            return render(request, 'solicitacao/index.html', contexto)
        else:
            msg_erro = 'Usuário não existe ou senha e usuário não conferem.'
            return render(request, 'solicitacao/login.html', {'msg_erro': msg_erro})
    else:

        if request.user.is_authenticated:
            username = request.GET.get('username')
            contexto = {'username': username, 'autenticado': True}
            return render(request, 'solicitacao/index.html', contexto)
        else:
            return render(request, 'solicitacao/login.html')


# Desloga o usuário do sistema
def logout_usuario(request):

    if request.user.is_authenticated:
        logout(request)

    return render(request, 'solicitacao/index.html')


# Cadastra o usuário
def signup(request):
    autenticado = request.user.is_authenticated
    username = request.user.username

    # Somente usuários autorizados podem cadastrar um novo usuário no sistema
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    if request.method == "POST":
        usuario = FormUsuario(request.POST)

        if usuario.is_valid():
            # Nome, senha e email
            nome_login = usuario.cleaned_data.get('nome_login').lower()
            primeiro_nome = usuario.cleaned_data.get('primeiro_nome')
            ultimo_nome = usuario.cleaned_data.get('ultimo_nome')
            senha = usuario.cleaned_data.get('senha')
            conf_senha = usuario.cleaned_data.get('conf_senha')
            email = usuario.cleaned_data.get('email')
            setor = usuario.cleaned_data.get('setor')
            gerencia = usuario.cleaned_data.get('gerencia')

            # Validações dos campos
            if User.objects.filter(username=nome_login).exists():
                msg_erro = 'Usuário já cadastrado. Escolha outro nick, por favor.'
            elif User.objects.filter(email=email).exists():
                msg_erro = 'E-mail já cadastrado. Escolha outro e-mail, por favor.'
            elif senha != conf_senha:
                msg_erro = 'Senhas não conferem.'
            elif len(senha) < 6:
                msg_erro = 'Sua senha deve possuir 6 caracteres no mínimo.'
            elif len(nome_login) < 3:
                msg_erro = 'Seu nome de usuário e deve possuir 3 caracteres no mínimo.'
            elif len(primeiro_nome) < 3 or len(ultimo_nome) < 3:
                msg_erro = 'Informe o seu nome sem abreviações ou apelidos, por favor.'
            elif not ModelSetor.objects.filter(nome=setor).exists():
                msg_erro = 'Este setor não existe ou não está registrado no sistema.'
            else:

                # Criação do novo usuário
                novo_usuario = User.objects.create_user(nome_login, email)
                novo_usuario.set_password(senha)
                novo_usuario.first_name = primeiro_nome
                novo_usuario.last_name = ultimo_nome
                setor_bd = ModelSetor.objects.get(nome=setor)
                ModelPerfil.objects.create(user=novo_usuario, setor=setor_bd)
                novo_usuario.save()
                msg_sucesso = 'Usuário cadastrado com sucesso!'
                contexto = {
                    'msg_sucesso': msg_sucesso,
                    'username': username,
                    'autenticado': autenticado
                }

                # Se passou por todos os critérios
                return render(request, 'solicitacao/signup.html', contexto)

            # Se não passou pelos critérios
            contexto = {
                'username': username,
                'autenticado': autenticado,
                'msg_erro': msg_erro,
                'nome_login': nome_login,
                'primeiro_nome': primeiro_nome,
                'ultimo_nome': ultimo_nome,
                'email': email, 'setor': setor,
                'gerencia': gerencia,
            }
            return render(request, 'solicitacao/signup.html', contexto)

        # Se o formulário for inválido
        else:
            msg_erro = 'Preencha os campos corretamento, por favor.'
            contexto = {
                'msg_erro': msg_erro,
                'username': username,
                'autenticado': autenticado
            }
            return render(request, 'solicitacao/signup.html', contexto)

    # GET
    else:
        contexto = {'username': username, 'autenticado': autenticado}
        return render(request, 'solicitacao/signup.html', contexto)


# Exibe informações do perfil do usuário
def perfil(request):
    autenticado = request.user.is_authenticated

    if not autenticado:
        return render(request, 'solicitacao/login.html')

    if request.method == "GET":
        username = request.user.username
        usuario = User.objects.get(username__exact=username)

        contexto = {
            'username': username,
            'autenticado': autenticado,
            'usuario': usuario
        }

        return render(request, 'solicitacao/perfil-usuario.html', contexto)

    # POST
    else:
        form_usuario = FormUsuario(request.POST)
        if form_usuario.is_valid():
            username = form_usuario.cleaned_data.get('nome_login')
            email = form_usuario.cleaned_data.get('email')
            senha = form_usuario.cleaned_data.get('senha')
            conf_senha = form_usuario.cleaned_data.get('conf_senha')
            usuario_bd = User.objects.get(username__exact=username)
            valid_email = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

            # Validação dos campos
            if senha != conf_senha:
                msg_erro = 'Senhas não conferem.'
            elif len(senha) < 6:
                msg_erro = 'Sua senha deve possuir 6 caracteres no mínimo.'
            elif not re.match(valid_email, email):
                msg_erro = 'E-mail inválido.'
            else:
                # Atualiza os dados
                usuario_bd.set_password(senha)
                usuario_bd.email = email
                usuario_bd.save()
                msg_sucesso = 'Dados atualizados com sucesso!'

                contexto = {
                        'msg_sucesso': msg_sucesso,
                        'username': username,
                        'autenticado': autenticado,
                        'usuario': usuario_bd
                }

                return render(request, 'solicitacao/perfil-usuario.html', contexto)

            # Se houve erro no preenchimento (ex.: e-mail inválido)
            contexto = {
                'msg_erro': msg_erro,
                'username': username,
                'autenticado': autenticado,
                'usuario': usuario_bd
            }

            return render(request, 'solicitacao/perfil-usuario.html', contexto)

        # Se o formulário for inválido
        username = request.user.username

        contexto = {
            'msg_erro': 'Ocorreu um erro. Certifique-se de ter preenchido os dados corretamente',
            'username': username,
            'autenticado': request.user.is_authenticated,
            'usuario': User.objects.get(username__exact=username)
        }

        return render(request, 'solicitacao/perfil-usuario.html', contexto)


# Cadastra a solicitação
def cadastro(request):
    autenticado = request.user.is_authenticated

    if autenticado:
        username = request.user.username
        usuario = User.objects.get(username__exact=username)
        sucesso = -1

        if request.method == "POST":
            formulario = FormSolicitacao(request.POST)
            if formulario.is_valid():
                formulario.save()
                sucesso = 0  # OK
            else:
                sucesso = 1  # ERRO

        contexto = {
            'username': username,
            'autenticado': autenticado,
            'usuario': usuario,
            'sucesso': sucesso
        }

        return render(request, 'solicitacao/cadastro.html', contexto)
    else:
        return render(request, 'solicitacao/login.html')


# Exibe a lista de solicitações
def lista_solicitacoes(request):
    autenticado = request.user.is_authenticated

    if autenticado:
        username = request.user.username
        solicitacoes = ModelSolicitacao.objects.all()

        if len(solicitacoes) > 0:
            # Ordem descendente
            solicitacoes = reversed(solicitacoes)

        contexto = {
            'username': username,
            'autenticado': autenticado,
            'solicitacoes': solicitacoes
        }

        return render(request, 'solicitacao/lista-solicitacoes.html', contexto)
    else:
        return render(request, 'solicitacao/login.html')


# Exibe a lista de solicitações
def lista_avaliacoes(request):
    autenticado = request.user.is_authenticated

    # Somente usuários autorizados podem visualizar a lista de avaliações
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    username = request.user.username
    avaliacoes = ModelAvaliacao.objects.all()

    if len(avaliacoes) > 0:
        # Ordem descendente
        avaliacoes = reversed(avaliacoes)

    contexto = {
        'username': username,
        'autenticado': autenticado,
        'avaliacoes': avaliacoes
    }

    return render(request, 'solicitacao/lista-avaliacoes.html', contexto)


# Cadastra a avaliação de uma solicitação
def avaliar(request, solicitacao_id):
    autenticado = request.user.is_authenticated
    sucesso = -1

    # Somente usuários autorizados podem avaliar uma solicitação
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    username = request.user.username
    responsavel = User.objects.get(username=username)
    nome_responsavel = responsavel.first_name + ' ' + responsavel.last_name

    try:
        solicitacao = ModelSolicitacao.objects.get(pk=solicitacao_id)
    except ModelSolicitacao.DoesNotExist:
        return render(request, 'solicitacao/index.html', {'username': username, 'autenticado': autenticado})

    if request.method == "POST":
        formulario = FormAvaliacao(request.POST)

        if formulario.is_valid():
            viabilidade = formulario.cleaned_data.get('viabilidade')
            if viabilidade.lower() == "sim":
                solicitacao.status = "viável"
            else:
                solicitacao.status = "inviável"

            formulario.save()
            solicitacao.save()
            sucesso = 0
        else:
            sucesso = 1
            try:
                formulario.save()
            except ValueError:
                # Avaliação já feita, código = 2
                sucesso = 2

    contexto = {
        'sucesso': sucesso,
        'nome_responsavel': nome_responsavel,
        'username': username,
        'autenticado': autenticado,
        'solicitacao': solicitacao
    }

    return render(request, 'solicitacao/avaliacao.html', contexto)


# Visualizar solicitação
def visualizar(request, solicitacao_id):
    autenticado = request.user.is_authenticated

    if autenticado:
        username = request.user.username
        solicitacao = ModelSolicitacao.objects.get(pk=solicitacao_id)

        contexto = {
            'username': username,
            'autenticado': autenticado,
            'solicitacao': solicitacao
        }

        return render(request, 'solicitacao/visualizar.html', contexto)
    else:
        return render(request, 'solicitacao/login.html')


# Deletar Solicitação
def del_solicitacao(request, solicitacao_id):
    autenticado = request.user.is_authenticated

    # Somente usuários autorizados podem deletar uma solicitação
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    username = request.user.username

    try:
        solicitacao = ModelSolicitacao.objects.get(pk=solicitacao_id)
        solicitacao.delete()
        msg = 'Solicitação ' + str(solicitacao_id) + ' deletada com sucesso.'
    except ModelSolicitacao.DoesNotExist:
        return render(request, 'solicitacao/index.html', {'username': username, 'autenticado': autenticado})

    solicitacoes = ModelSolicitacao.objects.all()

    if len(solicitacoes) > 0:
        # Ordem descendente
        solicitacoes = reversed(solicitacoes)

    contexto = {
        'username': username,
        'autenticado': autenticado,
        'solicitacao': solicitacao,
        'solicitacoes': solicitacoes,
        'msg': msg
    }

    return render(request, 'solicitacao/lista-solicitacoes.html', contexto)


# Visualização de uma avaliação
def avaliacao_visualizar(request, avaliacao_id):
    autenticado = request.user.is_authenticated

    # Somente usuários autorizados podem visualizar uma avaliação
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    username = request.user.username
    avaliacao = ModelAvaliacao.objects.get(pk=avaliacao_id)

    contexto = {
        'username': username,
        'autenticado': autenticado,
        'avaliacao': avaliacao
    }

    return render(request, 'solicitacao/avaliacao-visualizar.html', contexto)


# Deleta uma avaliação
def del_avaliacao(request, avaliacao_id):
    autenticado = request.user.is_authenticated

    # Somente usuários autorizados podem deletar uma avaliação
    if not autenticado:
        return render(request, 'solicitacao/login.html')
    if not membro_avaliacao(request):
        logout(request)
        return render(request, 'solicitacao/login.html')

    username = request.user.username

    try:
        avaliacao = ModelAvaliacao.objects.get(pk=avaliacao_id)
        avaliacao.delete()
        msg = 'Avaliação ' + str(avaliacao_id) + ' deletada com sucesso.'
    except ModelAvaliacao.DoesNotExist:
        return render(request, 'solicitacao/index.html', {'username': username, 'autenticado': autenticado})

    avaliacoes = ModelAvaliacao.objects.all()

    if len(avaliacoes) > 0:
        # Ordem descendente
        avaliacoes = reversed(avaliacoes)

    contexto = {
        'username': username,
        'autenticado': autenticado,
        'avaliacao': avaliacao,
        'avaliacoes': avaliacoes,
        'msg': msg
    }

    return render(request, 'solicitacao/lista-avaliacoes.html', contexto)
