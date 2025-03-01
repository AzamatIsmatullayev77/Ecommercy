from baton.autodiscover import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from user import views
from user.views import SimpleLoginView,SimpleLogoutView,ForgotPasswordView,RegisterView
app_name = 'user'
urlpatterns = [
       path('simple-login/', SimpleLoginView.as_view(), name='simple_login'),
       path('simple-logout/',SimpleLogoutView.as_view() , name='simple_logout'),
       path('simple-register/',RegisterView.as_view(),name='simple_register'),
       path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
       path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
       path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
]
