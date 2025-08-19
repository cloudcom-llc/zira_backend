from django.urls import path
from .views import PaymentUZSView, PaymentUSDView, PaymentNotifyView, PaymentStatusView

urlpatterns = [
    path('api/payment/uzs/', PaymentUZSView.as_view(), name='payment_uzs'),
    path('api/payment/usd/', PaymentUSDView.as_view(), name='payment_usd'),
    path('api/payment/notify/', PaymentNotifyView.as_view(), name='payment_notify'),
    path('api/payment/status/<int:purchase_id>/', PaymentStatusView.as_view(), name='payment_status'),
]