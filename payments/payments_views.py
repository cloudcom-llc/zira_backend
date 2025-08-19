from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketPurchaseSerializer
from .services import OCTOPaymentService
from .models import TicketPurchase

class PaymentUZSView(APIView):
    """API для оплаты в сумах (Humo/Uzcard)"""
    
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            octo_service = OCTOPaymentService()
            result = octo_service.create_payment_uzs(serializer.validated_data)
            
            if result['success']:
                return Response({
                    'success': True,
                    'payment_url': result['payment_url'],
                    'purchase_id': result['purchase_id'],
                    'message': 'Платеж создан успешно'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentUSDView(APIView):
    """API для оплаты в долларах (Bank Card)"""
    
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            octo_service = OCTOPaymentService()
            result = octo_service.create_payment_usd(serializer.validated_data)
            
            if result['success']:
                return Response({
                    'success': True,
                    'payment_url': result['payment_url'],
                    'purchase_id': result['purchase_id'],
                    'amount_usd': result['amount_usd'],
                    'message': 'Платеж создан успешно'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentNotifyView(APIView):
    """Webhook для уведомлений от OCTO о статусе платежа"""
    
    def post(self, request):
        try:
            # Получаем данные от OCTO
            notification_data = request.data
            octo_payment_uuid = notification_data.get('octo_payment_UUID')
            
            if not octo_payment_uuid:
                return Response({'error': 'Missing payment UUID'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Находим платеж в БД
            try:
                purchase = TicketPurchase.objects.get(octo_payment_uuid=octo_payment_uuid)
            except TicketPurchase.DoesNotExist:
                return Response({'error': 'Purchase not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Проверяем статус платежа через OCTO API
            octo_service = OCTOPaymentService()
            payment_status = octo_service.verify_payment(octo_payment_uuid)
            
            if payment_status and payment_status.get('error') == 0:
                data = payment_status.get('data', {})
                if data.get('status') == 'succeeded':
                    purchase.status = 'completed'
                elif data.get('status') == 'failed':
                    purchase.status = 'failed'
                purchase.save()
            
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentStatusView(APIView):
    """API для проверки статуса платежа"""
    
    def get(self, request, purchase_id):
        try:
            purchase = TicketPurchase.objects.get(id=purchase_id)
            return Response({
                'purchase_id': purchase.id,
                'status': purchase.status,
                'tariff': purchase.tariff,
                'full_name': purchase.full_name,
                'amount_uzs': purchase.amount_uzs,
                'amount_usd': purchase.amount_usd,
                'created_at': purchase.created_at
            }, status=status.HTTP_200_OK)
        except TicketPurchase.DoesNotExist:
            return Response({'error': 'Purchase not found'}, status=status.HTTP_404_NOT_FOUND)