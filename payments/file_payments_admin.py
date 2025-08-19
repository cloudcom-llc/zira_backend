from django.contrib import admin
from .models import TicketPurchase

@admin.register(TicketPurchase)
class TicketPurchaseAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'tariff', 'phone_number', 'payment_type', 'amount_uzs', 'status', 'created_at']
    list_filter = ['tariff', 'payment_type', 'status', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone_number']
    readonly_fields = ['octo_payment_uuid', 'octo_transaction_id', 'created_at', 'updated_at']
    
    # Отключаем возможность добавления/удаления/изменения
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # Показываем только успешно оплаченные билеты
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='completed')