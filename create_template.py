content = """{% extends 'base.html' %}
{% block title %}{{ event.title }}{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto bg-card rounded-2xl overflow-hidden shadow-2xl p-8">
<h1 class="text-4xl font-black text-white mb-4">{{ event.title }}</h1>
<p class="text-gray-400 mb-2">{{ event.venue }} - {{ event.date }}</p>
<p class="text-gray-300 mb-6">{{ event.description }}</p>
<form action="/checkout/" method="POST" class="bg-dark p-6 rounded-xl">
{% csrf_token %}
<input type="hidden" name="event_id" value="{{ event.id }}">
<div class="mb-4">
<label class="block text-gray-400 mb-2">Tipo de Entrada</label>
<select name="ticket_type_id" class="w-full bg-gray-800 text-white p-2 rounded" required>
{% for ticket in event.ticket_types.all %}
<option value="{{ ticket.id }}">{{ ticket.name }} - ${{ ticket.price }} ({{ ticket.stock }} disponibles)</option>
{% endfor %}
</select>
</div>
<div class="mb-4">
<label class="block text-gray-400 mb-2">Cantidad</label>
<select name="quantity" class="w-full bg-gray-800 text-white p-2 rounded">
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
</select>
</div>
<button type="submit" class="w-full bg-primary text-white font-bold py-3 rounded-lg">IR A PAGAR</button>
</form>
</div>
{% endblock %}"""

with open('templates/event_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("event_detail.html created!")
