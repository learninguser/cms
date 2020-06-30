from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog import models

# Apply summernote to all TextField in model.
# class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
#     summernote_fields = '__all__'

class CategoryAdmin(SummernoteModelAdmin):
    search_fields = ('name',)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'category', 'author', 'status')
    search_fields = ('title', 'category__name', 'author__username')
    list_filter = ('status', 'category')
    autocomplete_fields = ('category',)
    select_related = ('category','author')
    list_per_page = 10

# Register your models here.
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)