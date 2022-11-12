from django.contrib import admin
from .models import BonusCode
from django.utils.html import mark_safe

#НЕ ИСПОЛЬЗУЕТСЯ


class MyAdminSite(admin.AdminSite):
    site_header = '@fandydev2341bot админка'


admin_site = MyAdminSite(name='myadmin')

'''
class BonusAdmin(admin.ModelAdmin):
    fields = ('bonus_code', 'referals', 'creation_date', "code_level", "coment")
    readonly_fields = ('creation_date', 'referals', )
    list_display_links = ('bonus_code',)
    list_display = ('bonus_code', 'creation_date')
    list_filter = ('bonus_code', 'creation_date')

    @admin.display
    def referals(self, obj):
        return mark_safe(f'<a href="/admin/users/user_new/?ref_code={obj.bonus_code}"><p>Список пользователей</p></a>')
'''
#admin.site.register(BonusCode, BonusAdmin)
admin.site.register(BonusCode)

