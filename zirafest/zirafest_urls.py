from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

admin.site.site_header = "Zirafest Admin"
admin.site.site_title = "Zirafest Admin Portal"
admin.site.index_title = "Добро пожаловать в панель управления Zirafest"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payments.urls')),
    # Маршруты для фронтенда (можете настроить под ваш React роутинг)
    path('payment-success/', TemplateView.as_view(template_name='payment_success.html'), name='payment_success'),
]