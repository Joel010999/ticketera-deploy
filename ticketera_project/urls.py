from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import HomeView, EventDetailView
from orders.views import CheckoutView, payment_success, payment_failure

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout_start'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-failure/', payment_failure, name='payment_failure'),
    # path('orders/', include('orders.urls')),
    # path('users/', include('users.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
