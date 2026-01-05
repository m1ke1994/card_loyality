from django.urls import path

from .views import CheckoutView, TokenIssueView, TokenVerifyView

urlpatterns = [
    path("tokens/issue", TokenIssueView.as_view()),
    path("tokens/verify", TokenVerifyView.as_view()),
    path("visits/checkout", CheckoutView.as_view()),
]
