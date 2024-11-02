from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Projeto, Produto, CustomUser
from .formularios import ProjectoAdminForm

from django.utils.safestring import mark_safe

# Register your models here.
from django.contrib.auth.models import Group
admin.site.unregister(Group)

class ProdutoAdmin(admin.ModelAdmin):
    pass

class ProjetoAdmin(admin.ModelAdmin):
    form = ProjectoAdminForm
    # model = Projeto

    list_display = ('nome', 'start', 'acao')
    filter_horizontal = ('produto', 'fornecedor')

    def acao(self, obj):
         return mark_safe(f'<a href="/gerenciar/{obj.id}">Gerenciar</a>')

    

class CustomUserAdmin(UserAdmin):

    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        (('Dados Fornecedor'), {'fields': ('first_name', 'last_name', 'email', 'nome_fornecedor', 'contrato')}),
        (('Cadastro'), {'fields': ('is_staff', 'is_superuser', 'is_active')}),

    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
