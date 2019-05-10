from django.utils.html import format_html
from django.contrib import admin
from .models import Language, Repository

class RepositoryInline(admin.TabularInline):
    model = Repository

    verbose_name_plural = 'Repositories'
    readonly_fields = ('owner', 'avatar', 'name', 'description', 'forks', 'stars',)
    exclude = ('id',)
    ordering = ('-stars',)
    can_delete = False

    def avatar(self, obj):
        return format_html('<img src="{}" height="40"/>'.format(obj.owner_avatar))

    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            return obj.repositories.count()
        else:
            return 0


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'repositories',)

    inlines = [
        RepositoryInline,
    ]

    def repositories(self, obj):
        return obj.repositories.count()