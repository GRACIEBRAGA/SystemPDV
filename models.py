from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=20)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    cod_produto = models.IntegerField() 
    nome = models.CharField(max_length=255)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    def __str__(self):
        return self.nome

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def get_total(self):
        total = sum(item.get_subtotal() for item in self.itens.all())
        return total - self.desconto

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    

    def get_subtotal(self):
        return self.produto.preco * self.quantidade


    def __str__(self):
        return f"{self.produto.nome} ({self.quantidade})"
    

class Pagamento(models.Model):
    id_pagamento = models.CharField(max_length=400)
    pedido = models.ForeignKey(ItemVenda, null=True, blank=True, on_delete=models.SET_NULL)
    aprovado = models.BooleanField(default=False)

class NotaFiscalCF(models.Model):
    pedido = models.ForeignKey(ItemVenda, null=True, blank=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)

class EmissaoNotaFiscal(models.Model):
    pedido = models.ForeignKey(ItemVenda, null=True, blank=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
