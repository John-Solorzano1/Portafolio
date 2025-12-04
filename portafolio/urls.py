from django.urls import path
from .views.home import HomeView
from .views.contacto import ContactoView

urlpatterns = [
    path('', HomeView.as_view() , name = 'home'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
]