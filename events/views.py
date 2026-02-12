from django.views.generic import ListView, DetailView
from .models import Event

class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    ordering = ['date']
    
    def get_queryset(self):
        # Only show future events? For now all.
        return Event.objects.all().order_by('date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'
