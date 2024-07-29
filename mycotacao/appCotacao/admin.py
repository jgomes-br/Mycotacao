from django.contrib import admin

from .models import Projeto, Produto, Fornecedor
from .formularios import ProjectoAdminForm

from django.utils.safestring import mark_safe

# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    pass

class FornecedorAdmin(admin.ModelAdmin):
    pass


class ProjetoAdmin(admin.ModelAdmin):
    form = ProjectoAdminForm
    model = Projeto

    list_display = ('nome', 'start', 'acao')
    # list_display_links  = ('nome', 'edit', )

    def acao(self, obj):
         return mark_safe(f'<a href="/gerenciar/{obj.id}">Gerenciar</a>')

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
