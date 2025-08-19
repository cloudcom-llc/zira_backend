import requests
import json
from datetime import datetime
from django.conf import settings
from .models import TicketPurchase

class OCTOPaymentService:
    def __init__(self):
        self.base_url = settings.OCTO_BASE_URL
        self.shop_id = settings.OCTO_SHOP_ID
        self.secret = settings.OCTO_SECRET

    def create_payment_uzs(self, purchase_data):
        """Создание платежа в сумах (Humo/Uzcard)"""
        tariff = purchase_data['tariff']
        amount = settings.TICKET_PRICES[tariff]
        
        # Создаем запись в БД
        purchase = TicketPurchase.objects.create(
            tariff=tariff,
            first_name=purchase_data['first_name'],
            last_name=purchase_data['last_name'],
            phone_number=purchase_data['phone_number'],
            payment_type='uzs_local',
            amount_uzs=amount
        )

        # Данные для OCTO API
        payment_data = {
            "octo_shop_id": self.shop_id,
            "octo_secret": self.secret,
            "shop_transaction_id": f"zirafest_{purchase.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "auto_capture": True,
            "test": False,  # Поставьте True для тестирования
            "init_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_data": {
                "user_id": f"customer_{purchase.id}",
                "phone": purchase_data['phone_number'],
                "email": "a.kim@jowi.app"
            },
            "total_sum": amount,
            "currency": "UZS",
            "description": f"Билет {tariff.upper()} на Zirafest",
            "basket": [
                {
                    "position_desc": f"Билет {tariff.upper()} на Zirafest",
                    "count": 1,
                    "price": amount,
                    "spic": "10305011001000000",
                    "inn": "207096044",
                    "package_code": "1546392",
                    "nds": 1
                }
            ],
            "payment_methods": [
                {"method": "humo"},
                {"method": "uzcard"}
            ],
            "return_url": "https://zira.snts.uz/payment-success",
            "notify_url": "https://zira.snts.uz/api/payment/notify",
            "language": "uz",
            "ttl": 15
        }

        try:
            response = requests.post(
                f"{self.base_url}/prepare_payment",
                json=payment_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('error') == 0:
                    # Обновляем запись в БД
                    purchase.octo_payment_uuid = result['data']['octo_payment_UUID']
                    purchase.octo_transaction_id = result['data']['shop_transaction_id']
                    purchase.save()
                    
                    return {
                        'success': True,
                        'payment_url': result['data']['octo_pay_url'],
                        'purchase_id': purchase.id
                    }
                else:
                    purchase.status = 'failed'
                    purchase.save()
                    return {'success': False, 'error': result.get('errMessage', 'Ошибка создания платежа')}
            else:
                purchase.status = 'failed'
                purchase.save()
                return {'success': False, 'error': 'Ошибка соединения с платежным сервисом'}
        except Exception as e:
            purchase.status = 'failed'
            purchase.save()
            return {'success': False, 'error': str(e)}

    def create_payment_usd(self, purchase_data):
        """Создание платежа в долларах (Bank Card)"""
        tariff = purchase_data['tariff']
        amount_uzs = settings.TICKET_PRICES[tariff]
        amount_usd = round(amount_uzs / settings.USD_TO_UZS_RATE, 2)
        
        # Создаем запись в БД
        purchase = TicketPurchase.objects.create(
            tariff=tariff,
            first_name=purchase_data['first_name'],
            last_name=purchase_data['last_name'],
            phone_number=purchase_data['phone_number'],
            payment_type='usd_bankcard',
            amount_uzs=amount_uzs,
            amount_usd=amount_usd
        )

        # Данные для OCTO API (аналогично, но с USD)
        payment_data = {
            "octo_shop_id": self.shop_id,
            "octo_secret": self.secret,
            "shop_transaction_id": f"zirafest_usd_{purchase.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "auto_capture": True,
            "test": False,
            "init_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_data": {
                "user_id": f"customer_{purchase.id}",
                "phone": purchase_data['phone_number'],
                "email": "a.kim@jowi.app"
            },
            "total_sum": int(amount_usd * 100),  # В центах для USD
            "currency": "USD",
            "description": f"Билет {tariff.upper()} на Zirafest",
            "basket": [
                {
                    "position_desc": f"Билет {tariff.upper()} на Zirafest",
                    "count": 1,
                    "price": int(amount_usd * 100),
                    "spic": "10305011001000000",
                    "inn": "207096044",
                    "package_code": "1546392",
                    "nds": 1
                }
            ],
            "payment_methods": [
                {"method": "bank_card"}
            ],
            "return_url": "https://zira.snts.uz/payment-success",
            "notify_url": "https://zira.snts.uz/api/payment/notify",
            "language": "en",
            "ttl": 15
        }

        try:
            response = requests.post(
                f"{self.base_url}/prepare_payment",
                json=payment_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('error') == 0:
                    purchase.octo_payment_uuid = result['data']['octo_payment_UUID']
                    purchase.octo_transaction_id = result['data']['shop_transaction_id']
                    purchase.save()
                    
                    return {
                        'success': True,
                        'payment_url': result['data']['octo_pay_url'],
                        'purchase_id': purchase.id,
                        'amount_usd': amount_usd
                    }
                else:
                    purchase.status = 'failed'
                    purchase.save()
                    return {'success': False, 'error': result.get('errMessage', 'Ошибка создания платежа')}
            else:
                purchase.status = 'failed'
                purchase.save()
                return {'success': False, 'error': 'Ошибка соединения с платежным сервисом'}
        except Exception as e:
            purchase.status = 'failed'
            purchase.save()
            return {'success': False, 'error': str(e)}

    def verify_payment(self, octo_payment_uuid):
        """Проверка статуса платежа"""
        try:
            response = requests.post(
                f"{self.base_url}/verificationInfo/",
                json={"octo_payment_UUID": octo_payment_uuid},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result
            return None
        except Exception as e:
            return None