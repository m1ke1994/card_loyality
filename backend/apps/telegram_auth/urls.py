from django.urls import path

from .views import LogoutView, RefreshView, TelegramConsumeView, TelegramSessionStartView

urlpatterns = [
    path("telegram/session/start", TelegramSessionStartView.as_view()),
    path("auth/telegram/consume", TelegramConsumeView.as_view()),
    path("auth/refresh", RefreshView.as_view(), name="token_refresh"),
    path("auth/logout", LogoutView.as_view()),
]
