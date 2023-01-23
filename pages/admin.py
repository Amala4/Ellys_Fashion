from django.contrib import admin
from .models import  Contact, Subscribers


class ContactAdmin (admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message' )
    list_display_links = ('message',)
    search_fields = ('name', 'email', 'message')
    list_per_page = 100


admin.site.register(Contact, ContactAdmin)



class SubscribersAdmin (admin.ModelAdmin):
    list_display = ('email',)
    readonly_fields = ('email',)
    search_fields = ('email',)
    list_per_page = 100


admin.site.register(Subscribers, SubscribersAdmin)



