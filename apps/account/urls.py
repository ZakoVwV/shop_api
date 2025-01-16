from django.urls import path

from .views import RegisterView, ActivateView, LoginView, RefreshView, LogOutView, ResetPasswordView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh-token/', RefreshView.as_view()),
    path('logout/',LogOutView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view())
]