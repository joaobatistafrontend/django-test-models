from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Agendamento

def contato(request):
     if(request.method) == 'POST':
          form = Agendamento(request.POST)
          if form.is_valid():
               form.send_email()
               form = Agendamento()
     else:
          form = Agendamento()
     context = {
          'form' : form
     }
     return render(request, 'form.html', context)
               
