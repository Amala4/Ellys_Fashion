from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('terms-and-condition', views.terms, name ='terms'),
    path('privacy-policy', views.privacy, name ='privacy'),
    path('about', views.about, name ='about'),
    path('contact', views.contact, name ='contact'),
    path('subscribe', views.subscribe, name ='subscribe'),
]
