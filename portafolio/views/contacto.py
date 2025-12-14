from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from portafolio.forms.contacto_forms import ContactForm

class ContactoView(FormView):
    template_name = "index.html"
    form_class = ContactForm
    success_url = reverse_lazy('home')
    
    def form_valid(self , form):
        nombre = form.cleaned_data['nombre']
        email = form.cleaned_data['email']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        
        cuerpo = (
            f"Nombre: {nombre}\n"
            f"Email: {email}\n\n"
            f"Mensaje:\n{mensaje}"
        )
        
        try:
            # Enviar mensaje al portafolio
            email_msg = EmailMessage(
                subject=f"[Contacto] {asunto}" if asunto else "[Contacto] Nuevo mensaje",
                body=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[email] if email else None,
            )
            email_msg.send(fail_silently=False)
            
            
            mensaje_auto = (
            "Hola,\n\n"
            "He recibido tu mensaje correctamente. Gracias por contactarme.\n"
            "Te responderé lo antes posible.\n\n"
            "Saludos cordiales,\n"
            "John Solórzano"
            )
            
            email_auto = EmailMessage(
                subject="Hemos recibido tu mensaje",
                body=mensaje_auto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email] if email else [],
            )
            email_auto.send(fail_silently=False)
            
            messages.success(self.request , "Mensaje enviado correctamente.Te contactaré pronto.")
        except Exception as e:
            print("ERROR SEND_MAIL:", e)
            messages.error(self.request, "Ocurrió un error al enviar el mensaje. Intenta otra vez.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrige los errores en el formulario.")
        return super().form_invalid(form)