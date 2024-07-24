from django.contrib import admin

from .models import Projeto, Produto, Fornecedor
from .formularios import ProjectoAdminForm

# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    pass

class FornecedorAdmin(admin.ModelAdmin):
    pass

class ProjetoAdmin(admin.ModelAdmin):
    form = ProjectoAdminForm
    model = Projeto

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
