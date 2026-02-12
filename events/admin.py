from django.contrib import admin
from .models import Event, TicketType

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [TicketTypeInline]
    list_display = ['title', 'date', 'venue']
    search_fields = ['title', 'description']

admin.site.register(TicketType)
