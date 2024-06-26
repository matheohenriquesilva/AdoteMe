from django.shortcuts import render, redirect
from divulgar.models import Pet, Raca
from django.contrib.messages import constants
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime
from django.core.mail import send_mail

# Create your views here.
def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status="P")
        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)
        if raca_filter:
            pets = pets.filter(raca_id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)
        return render (request, 'listar_pets.html', {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter})

def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.WARNING, 'Esse pet já foi adotado.')
        return redirect('/adotar')
    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=pet.usuario,
                          data=datetime.now())
    # Inicio - VERIFICANDO SE USUÁRIO JÁ SOLICITOU A ADOÇÃO DESSE PET.----------------------------------------------
    usuario_aux = PedidoAdocao.objects.filter(usuario=request.user.id)
    pet_aux = PedidoAdocao.objects.filter(pet=pet.first().id)
    if usuario_aux and pet_aux:
        messages.add_message(request, constants.WARNING, 'Você já socilitou a adoção desse pet.')
        return redirect('/adotar')
    # Fim - VERIFICANDO SE USUÁRIO JÁ SOLICITOU A ADOÇÃO DESSE PET.------------------------------------------------

    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção enviado com sucesso.')
    return redirect('/adotar')

def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    pet = Pet.objects.get(id=pedido.pet_id)

    if status == "A":
        pedido.status = 'AP'
        aux_str = 'Olá, sua adoção foi aprovada com sucesso...'
        pet.status = "A"
    elif status == "R":
        aux_str = 'Olá, sua adoção foi recusada...'
        pedido.status = "R"

    pedido.save()
    # Alterar status do Pet.
    email = send_mail(
        'Sua adoção foi processada!',
        aux_str,
        'adote@mail.com.br',
        [pedido.usuario.email,]
    )

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso!')
    return redirect('/divulgar/ver_pedido_adocao')
