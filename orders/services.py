from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Order, Ticket
from events.models import TicketType

def create_order(user, ticket_type_id, quantity):
    """
    Creates an order with atomic stock reservation.
    """
    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")

    with transaction.atomic():
        # Lock the ticket type row to prevent race conditions
        try:
            ticket_type = TicketType.objects.select_for_update().get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise ValidationError("Ticket type not found.")

        if not ticket_type.is_active:
             raise ValidationError("Ticket sale is not active.")

        if ticket_type.stock < quantity:
            raise ValidationError(f"Insufficient stock. Only {ticket_type.stock} left.")

        # Create Order (Pending Payment)
        order = Order.objects.create(
            user=user,
            ticket_type=ticket_type,
            quantity=quantity,
            total_price=ticket_type.price * quantity,
            status='PENDING'
        )

        # Deduct stock immediately (reservation)
        # If payment expires or is cancelled, this must be reversed.
        ticket_type.stock -= quantity
        ticket_type.save()

        return order

def confirm_order(order):
    """
    Called when payment is successful. Generates valid tickets.
    """
    with transaction.atomic():
        order.status = 'PAID'
        order.save()
        
        # Generate tickets
        for _ in range(order.quantity):
            Ticket.objects.create(order=order)

def cancel_order(order):
    """
    Called when payment fails or expires. Restores stock.
    """
    with transaction.atomic():
        if order.status == 'PENDING':
            ticket_type = order.ticket_type
            # Lock here too to be safe, though not strictly required if only adding
            ticket_type = TicketType.objects.select_for_update().get(id=ticket_type.id)
            
            ticket_type.stock += order.quantity
            ticket_type.save()
            
            order.status = 'CANCELLED'
            order.save()
