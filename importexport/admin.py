from django.contrib import admin

from importexport.models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'get_status_display', 'title', 'description', 'keywords', 'username', 'date'
    )
    list_filter = ('profile', 'status',)
    search_fields = ('title', 'description', 'keywords')
