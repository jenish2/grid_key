from django.urls import path
from .views import TransactionView, HoldingsView

urlpatterns = [path('add_transaction', TransactionView.as_view()), path('get_holdings', HoldingsView.as_view())]
