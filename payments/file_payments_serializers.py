from rest_framework import serializers
from .models import TicketPurchase

class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = ['tariff', 'first_name', 'last_name', 'phone_number']
    
    def validate_tariff(self):
        tariff = self.validated_data.get('tariff')
        if tariff not in ['standard', 'gold', 'platinum']:
            raise serializers.ValidationError("Некорректный тариф")
        return tariff