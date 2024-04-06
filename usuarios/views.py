from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/seus_pets')

    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        nome_usuario = request.POST.get('nome_usuario')
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")
        campos = [nome_usuario, sobrenome, nome, email, senha, confirmar_senha]
        for dado in campos:
            if len(dado.strip()) == 0:
                messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
                return render(request, 'cadastro.html')
        username_aux = User.objects.filter(username=nome_usuario)
        email_aux = User.objects.filter(email=email)
        if username_aux:
            messages.add_message(request, constants.ERROR, 'Esse nome de usuario já está em uso.')
            return render(request, 'cadastro.html')
        if email_aux:
            messages.add_message(request, constants.ERROR, 'Já existe usuario cadastrado com esse email.')
            return render(request, 'cadastro.html')
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 6 caracteres.')
            return render(request, 'cadastro.html')
        simbolos = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]
        numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        letras_upper =["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K",
                       "L", "Z", "X", "C", "V", "B", "N", "M", "Ç"]
        letras_lower = list()
        for l in letras_upper:
            letras_lower.append(l.lower())
        # ----------------------------------------------------
        letras_lower_aux = False
        for ll in letras_lower:
            if senha.find(ll) != -1:
                letras_lower_aux = True
        simbolos_aux = False
        for s in simbolos:
            if senha.find(s) != -1:
                simbolos_aux = True
        letras_upper_aux = False
        for lu in letras_upper:
            if senha.find(lu) != -1:
                letras_upper_aux = True
        numeros_aux = False
        for nu in numeros:
            if senha.find(str(nu)) != -1:
                numeros_aux = True
        # ---------------------------------------------------
        if simbolos_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos um caractere especial...')
            return render(request, 'cadastro.html')
        if letras_upper_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos uma letra maiúscula...')
            return render(request, 'cadastro.html')
        if letras_lower_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos uma letra minúscula...')
            return render(request, 'cadastro.html')
        if numeros_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos um número...')
            return render(request, 'cadastro.html')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não correspondem.')
            return render(request, 'cadastro.html')
        try:
            user = User.objects.create_user(
                username = nome_usuario,
                first_name = nome,
                last_name = sobrenome,
                email = email,
                password = senha
            )
            # MSG SUCESSO
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return render(request, 'cadastro.html')
        except:
            #MSG ERRO
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return render(request, 'cadastro.html')

def logar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/seus_pets')

    if request.method == "GET":
        return render(request, 'login.html')
    else:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(username=nome, password=senha)

        if user is not None:
            login(request, user)
            return redirect('/divulgar/seus_pets')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos.')
            return render(request, 'login.html')

def sair(request):
    logout(request)
    return redirect('/auth/login')
# Create your views here.
def welcome(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'listar_pets.html')
        return render(request, 'welcome.html')

def admin(request):
    if request.method == "GET":
        return redirect('/admin')

def guia(request):
    if request.method == "GET":
        return HttpResponse("PÁGINA DE GUIA EM DESENVOLVIMENTO...")

def creditos(request):
    if request.method == "GET":
        return HttpResponse("PÁGINA DE CRÉDITOS EM DESENVOLVIMENTO...")
