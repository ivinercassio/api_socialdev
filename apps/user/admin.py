from django.contrib import admin

from .models import User

# Admin: configuração do painel Django para gerenciar users
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'public', 'about', 'tipo', 'creation_date']
    list_filter = ['tipo', 'username']                                                          
    search_fields = ['username', 'public', 'tipo', 'creation_date']                                   
    readonly_fields = ['tipo', 'creation_date']                                  