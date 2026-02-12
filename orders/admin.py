from django.contrib import admin
from .models import Order, Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ['unique_hash']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ticket_type', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [TicketInline]

admin.site.register(Ticket)
