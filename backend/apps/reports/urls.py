from django.urls import path

from .views import SummaryReportView, TransactionsReportView, VisitsReportView

urlpatterns = [
    path("admin/reports/summary", SummaryReportView.as_view()),
    path("admin/reports/visits", VisitsReportView.as_view()),
    path("admin/reports/transactions", TransactionsReportView.as_view()),
]
