from django.urls import path,include
from .views  import contato

urlpatterns = [
     path('',contato, name='index')
]
