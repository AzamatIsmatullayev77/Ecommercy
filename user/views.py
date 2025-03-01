import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from user.custom_token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib import messages


# Create your views here.

def simple_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('ecommerce:index')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Username or password is incorrect')
    context = {
        'form': form,
    }
    return render(request, 'user/login.html', context=context)


def simple_logout(request):
    logout(request)
    return render(request, 'user/logout.html')


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            # login(request, form)
            return redirect('ecommerce:index')
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context=context)


def forgot_password(request):
    return render(request, 'user/forgot-password.html')


from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, View
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class SimpleLoginView(View):
    template_name = 'user/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            send_mail(
                "Siz tizimga kirdingiz",
                "Hurmatli foydalanuvchi, siz tizimga muvaffaqiyatli kirdingiz.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            if user:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('ecommerce:index')
            else:
                messages.error(request, 'Email yoki parol noto‘g‘ri!')
                return redirect('user:simple_login')
        return render(request, self.template_name, {'form': form})


class SimpleLogoutView(View):
    template_name = 'user/logout.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('ecommerce:index')

    def form_valid(self, form):
        user = form.save()
        get_name_by_email = user.email.split('@')[0]
        user.set_password(form.cleaned_data['password1'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        email = user.email
        subject = 'Verify your email'
        message = render_to_string('user/email_verification/verify_email_message.html', {
            'request': requests.request,
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user), })
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
        email.content_subtype = 'html'
        email.send()
        data = 'We send your verification. Please check your email😁'
        return HttpResponse(f'<h2>{data}</h2>')

    def form_invalid(self, form):
        messages.error(self.request, 'password or email is incorrect')
        return super().form_invalid(form)


class ForgotPasswordView(View):
    template_name = 'user/forgot-password.html'

    def get(self, request):
        return render(request, self.template_name)


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('user:verify-email-complete')
    else:
        messages.warning(request, 'The link is invalid.')
        return render(request, 'user/email_verification/verify_email_confirm.html')


def verify_email_complete(request):
    return render(request, 'user/email_verification/verify_email_complate.html')
