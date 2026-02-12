from django.db import models
from django.conf import settings
from events.models import TicketType
import uuid

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    mp_preference_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

class Ticket(models.Model):
    order = models.ForeignKey(Order, related_name='tickets', on_delete=models.CASCADE)
    unique_hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)
    # Could store more metadata like QR code image path if generated statically, 
    # but generating on the fly is often better.

    def __str__(self):
        return f"Ticket {self.unique_hash} for Order #{self.order.id}"
