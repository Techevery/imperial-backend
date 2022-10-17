from django.contrib import admin
from .models import Property, Flat, AddPayment
# Register your models here.

class BookSlotAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


    #df



class SlotAdmin(admin.ModelAdmin):
    list_display = ['property_name']
    list_filter = ['property_name']
    search_fields = ['property_name']
admin.site.register(Property, SlotAdmin)
admin.site.register(Flat, BookSlotAdmin)
admin.site.register(AddPayment)

