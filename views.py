from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views.generic import ListView, TemplateView
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from .models import Cliente, Produto, Venda, ItemVenda
from .forms import ClienteForm, ProdutoForm, VendaForm, ItemVendaForm
from .models import *
from django.shortcuts import render, redirect
from .models import Venda, ItemVenda
from .forms import VendaForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit


def home(request):
    return render(request, 'homepage.html')


def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'cadastrar_cliente.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})


def realizar_venda(request):
    formset_itens = []
    ItemVendaFormSet = inlineformset_factory(Venda, ItemVenda, form=ItemVendaForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form_venda = VendaForm(request.POST)
        formset_itens = ItemVendaFormSet(request.POST)
        if form_venda.is_valid() and formset_itens.is_valid():
            venda = form_venda.save()
            formset_itens.instance = venda
            formset_itens.save()
            return redirect('finalizar_venda', venda_id=venda.id)
    else:
        form_venda = VendaForm()
        formset_itens = ItemVendaFormSet()

    context = {
        'form_venda': form_venda,
        'formset_itens': formset_itens,
    }
    return render(request, 'realizar_venda.html', context)


def emitir_nota_fiscal(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    itens = venda.itens.all()
    return render(request, 'emitir_nota_fiscal.html', {'venda': venda, 'itens': itens})



#def listar_vendas(request):
 #   vendas = Venda.objects.prefetch_related('itens__produto').all()
  #  return render(request, 'listar_vendas.html', {'vendas': vendas})

def listar_vendas(request):
    vendas = Venda.objects.all().prefetch_related('itens__produto')
    context = {
        'vendas': vendas
    }
    return render(request, 'listar_vendas.html', context)

def minha_conta(request):
    return render(request, 'usuario/minha_conta.html')


def login(request):
    return render(request, 'usuario/login.html')

#def emitir_nota_fiscal(request):
 #   if request.method == 'POST':
  #      form_venda = VendaForm(request.POST)
    # Lógica para emitir a nota fiscal
    # Isso pode envolver a integração com um sistema externo de emissão de notas

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def finalizar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    itens = venda.itens.all()

    context = {
        'venda': venda,
        'itens': itens,
    }
    return render(request, 'finalizar_venda.html', context)