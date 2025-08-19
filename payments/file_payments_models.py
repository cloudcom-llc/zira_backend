from django.db import models

class TicketPurchase(models.Model):
    TARIFF_CHOICES = [
        ('standard', 'Standard (2 млн сум)'),
        ('gold', 'Gold (3 млн сум)'),
        ('platinum', 'Platinum (10 млн сум)'),
    ]
    
    PAYMENT_TYPE_CHOICES = [
        ('uzs_local', 'UZS (Humo/Uzcard)'),
        ('usd_bankcard', 'USD (Bank Card)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Успешно оплачен'),
        ('failed', 'Ошибка'),
    ]

    # Основная информация
    tariff = models.CharField(max_length=20, choices=TARIFF_CHOICES, verbose_name='Тариф')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    
    # Информация об оплате
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name='Тип оплаты')
    amount_uzs = models.IntegerField(verbose_name='Сумма в сумах')
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Сумма в долларах')
    
    # OCTO данные
    octo_payment_uuid = models.CharField(max_length=200, null=True, blank=True, verbose_name='OCTO Payment UUID')
    octo_transaction_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='OCTO Transaction ID')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Покупка билета'
        verbose_name_plural = 'Покупки билетов'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_tariff_display()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"