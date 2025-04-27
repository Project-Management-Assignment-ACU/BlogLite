from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from .forms import ContactForm, UserRegistrationForm

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

class CustomLoginView(FormView):
    template_name = 'auth/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {username}!")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

def logout_view(request):
    """Simple logout view that renders a confirmation page and processes logout"""
    if request.method == 'POST':
        # User confirmed logout
        username = request.user.username  # Store before logout
        logout(request)
        messages.success(request, f"You have been logged out successfully.")
        return redirect('core:home')
    
    # GET request - show the logout confirmation page
    return render(request, 'auth/logout.html')

class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Account created successfully for {username}! You can now log in.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your registration. Please check the form and try again.")
        return super().form_invalid(form)
