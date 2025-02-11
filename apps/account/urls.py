from django.urls import path

from .views import RegisterView, ActivateView, LoginView, RefreshView, LogOutView, ResetPasswordView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', RefreshView.as_view(), name='refresh-token'),
    path('logout/',LogOutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm')
]