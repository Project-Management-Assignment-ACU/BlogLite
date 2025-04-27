from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        # Get form data
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        # Create email content
        email_subject = f"Contact Form: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.CONTACT_EMAIL]
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            # Add success message
            messages.success(
                self.request, 
                "Thank you for your message! We'll get back to you soon."
            )
        except Exception as e:
            # Log the error (in a real application)
            print(f"Email sending failed: {str(e)}")
            # Add error message
            messages.error(
                self.request, 
                "Sorry, there was a problem sending your message. Please try again later."
            )
            
        return super().form_valid(form)
