from django.db import models
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO



class Agendamento(models.Model):
     nome = models.CharField(max_length=100)
     email = models.EmailField(max_length=100)
     opcoes = models.CharField(max_length=100, choices=[
          ('Unidade de Placa de Carro', 'Unidade de Placa de Carro'),
          ('Par de Placa de Carro', 'Par de Placa de Carro'),
          ('Placa de Moto', 'Placa de Moto'),
     ])
     horario = models.TimeField()
     local = models.CharField(max_length=200)
     data = models.DateField()
     def enviar_email_com_pdf(self):
          assunto = 'Comprovante de Agendamento'

          # Criação de um arquivo PDF com os dados do agendamento
          buffer = BytesIO()
          doc = SimpleDocTemplate(buffer, pagesize=letter)
          styles = getSampleStyleSheet()
          elements = []

          elements.append(Paragraph('Comprovante de Agendamento', styles['Title']))
          elements.append(Spacer(1, 12))

          data_table = [
               ['Nome:', self.nome],
               ['Email:', self.email],
               ['Opções de Agendamento:', self.opcoes],
               ['Horário:', self.horario.strftime('%H:%M')],
               ['Local:', Paragraph(self.local, styles['Normal'])],
               ['Data de Agendamento:', self.data.strftime('%d/%m/%Y')],
          ]

          table = Table(data_table, colWidths=300, rowHeights=30)
          table.setStyle(TableStyle([
               ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
               ('GRID', (0, 0), (-1, -1), 1, colors.black),
          ]))

          elements.append(table)
          doc.build(elements)

          # Anexa o PDF ao e-mail
          buffer.seek(0)
          email = EmailMessage(
               subject=assunto,
               from_email='seu_email@gmail.com',  # Substitua pelo seu endereço de e-mail
               to=[self.email],
          )
          email.attach('comprovante.pdf', buffer.read(), 'application/pdf')
          email.send()