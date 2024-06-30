from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Venda)
admin.site.register(ItemVenda)
admin.site.register(NotaFiscalCF)
admin.site.register(EmissaoNotaFiscal)

