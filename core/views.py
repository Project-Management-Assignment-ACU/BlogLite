"""Temel uygulama view'larını içerir.

Bu modül, kullanıcı kimlik doğrulama ve ana sayfa gibi
temel uygulama işlevlerini sağlayan view'ları içerir.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import ContactForm

# Create your views here.


class HomeView(TemplateView):
    """Ana sayfa view'ı."""

    template_name = "core/home.html"


class AboutView(TemplateView):
    """Hakkımızda sayfası view'ı."""

    template_name = "about.html"


class ContactView(FormView):
    """İletişim formu view'ı."""

    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        """Form geçerliyse e-posta gönderir."""
        # Get form data
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

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
                self.request, "Thank you for your message! We'll get back to you soon."
            )
        except Exception as e:
            # Log the error (in a real application)
            print(f"Email sending failed: {str(e)}")
            # Add error message
            messages.error(
                self.request,
                "Sorry, there was a problem sending your message. Please try again later.",
            )

        return super().form_valid(form)


class LoginView(AuthLoginView):
    """Kullanıcı giriş view'ı."""

    template_name = "core/login.html"
    next_page = "home"


class LogoutView(AuthLogoutView):
    """Kullanıcı çıkış view'ı."""

    next_page = "home"


class RegisterView(CreateView):
    """Kullanıcı kayıt view'ı."""

    template_name = "core/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Form geçerliyse kullanıcıyı oluşturur ve giriş yapar."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Registration successful!")
        return response

    def form_invalid(self, form):
        """Form geçersizse hata mesajı gösterir."""
        messages.error(self.request, "Registration failed. Please check the form.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """Giriş yapmış kullanıcıları ana sayfaya yönlendirir."""
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    """Çıkış işlemini gerçekleştirir ve onay sayfasını gösterir."""
    if request.method == "POST":
        # User confirmed logout
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("core:home")

    # GET request - show the logout confirmation page
    return render(request, "auth/logout.html")
