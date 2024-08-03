from django.contrib import admin
from .models import Event, Feedback, Item

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')  # Add other fields as needed
    filter_horizontal = ('participants',)  # This allows for easier selection of participants

admin.site.register(Event, EventAdmin)
admin.site.register(Feedback)
admin.site.register(Item)