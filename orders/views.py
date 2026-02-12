import mercadopago
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from .models import Order
from .services import create_order
from django.core.exceptions import ValidationError

# Initialize Mercado Pago SDK
# Replace with your ACCESS_TOKEN from settings or env
sdk = mercadopago.SDK("TEST-3834674735234907-072018-86d11da9772d159a6745163533633632-156383182") 

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ticket_type_id = request.POST.get('ticket_type_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            # Atomic Order Creation
            order = create_order(request.user, ticket_type_id, quantity)
            
            # Create Mercado Pago Preference
            preference_data = {
                "items": [
                    {
                        "id": str(order.ticket_type.id),
                        "title": f"Entrada: {order.ticket_type.event.title} - {order.ticket_type.name}",
                        "quantity": order.quantity,
                        "currency_id": "ARS",
                        "unit_price": float(order.ticket_type.price)
                    }
                ],
                "payer": {
                    "name": request.user.full_name or request.user.username,
                    "email": request.user.email
                },
                "back_urls": {
                    "success": request.build_absolute_uri(reverse('payment_success')),
                    "failure": request.build_absolute_uri(reverse('payment_failure')),
                    "pending": request.build_absolute_uri(reverse('payment_failure'))
                },
                "auto_return": "approved",
                "external_reference": str(order.id)
            }
            
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            
            # Save preference ID to order
            order.mp_preference_id = preference['id']
            order.save()
            
            # Redirect to Mercado Pago Checkout
            return redirect(preference['init_point'])
            
        except ValidationError as e:
            messages.error(request, str(e))
            # Redirect back to event detail (needs event_id)
            # Simplification: redirect home or back if referer exists
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
            return redirect('home')

def payment_success(request):
    # Verify payment status using MP or just trust the redirect for MVP (Verification Plan has robust check)
    # Ideally, we check the status from the query params
    
    collection_status = request.GET.get('collection_status')
    external_ref = request.GET.get('external_reference')
    
    if collection_status == 'approved' and external_ref:
        try:
            order = Order.objects.get(id=external_ref)
            from .services import confirm_order
            confirm_order(order) # Confirm and generate tickets
            return render(request, 'success.html', {'order': order})
        except Order.DoesNotExist:
            pass
            
    return redirect('home')

def payment_failure(request):
    return render(request, 'failure.html')
