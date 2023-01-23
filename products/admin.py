from django.contrib import admin
from .models import ProductList, Category, Colour

class CategoryAdmin (admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)



class ColourAdmin (admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    list_per_page = 25

admin.site.register(Colour, ColourAdmin)



class ProductListAdmin (admin.ModelAdmin):
    list_display = ('id', 'name', 'size', 'price', 'is_published')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'colour', 'gender', 'size')
    list_editable = ('is_published',)
    search_fields = ('name', 'description')
    list_per_page = 25

admin.site.register(ProductList, ProductListAdmin)





