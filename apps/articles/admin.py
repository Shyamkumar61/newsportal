from django.contrib import admin
from .models import ArticleCategory, Article, ArticleTag, ArticleHistory, LeadNewsHistory, LeadNews, Page, District
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register your models here.

class ArticleCategoryAdmin(TreeAdmin):
    form = movenodeform_factory(ArticleCategory)
    list_display = ('name', 'name_en', 'slug')
    list_editable = ('name_en',)
    readonly_fields = ('slug',)

class ArticleAdmin(admin.ModelAdmin):

    list_filter = ('status', 'created', 'tags')
    list_display = ('__str__', 'status', 'slug', 'created', 'last_changed_date')
    list_editable = ('status',)
    readonly_fields = ('slug',)
    search_fields = ['title']
    autocomplete_fields = ['tags']

class ArticleAdminForm(forms.ModelForm):
    short_description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = '__all__'

class ArticleTagAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    search_fields = ('name', )
    readonly_fields = ('slug',)

class LeadNewsAdmin(admin.ModelAdmin):

    list_display = ('article', 'position', 'created')
    list_editable = ('position',)

class PageAdmin(admin.ModelAdmin):

    list_display = ('name', 'page_type', 'status', 'is_active')
    list_editable = ('status',)
    readonly_fields = ('is_active',)
    

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleHistory)
admin.site.register(LeadNewsHistory)
admin.site.register(LeadNews, LeadNewsAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(District)

