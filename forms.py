from django import forms
from django.forms import inlineformset_factory

from .models import Cliente, Produto, Venda, ItemVenda
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'email', 'telefone']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['cod_produto', 'nome', 'preco_compra', 'estoque', 'preco']

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'desconto']
ItemVendaFormSet = inlineformset_factory(Venda, ItemVenda, fields=('produto', 'quantidade'), extra=1, can_delete=True)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
    )
    password = forms.CharField(
        label=("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
    )
