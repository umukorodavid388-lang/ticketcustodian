from django.contrib import admin
from .models import *
from django.utils.html import format_html


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'ticket_type',
        'display_current_price',
        'display_phase',
        'created_at'
    )

    list_filter = ('ticket_type', 'created_at')
    search_fields = ('name',)

    readonly_fields = ('display_current_price', 'display_phase')

    fieldsets = (

        ("Basic Information", {
            'fields': ('name', 'ticket_type')
        }),

        ("Regular Ticket (Early Bird)", {
            'fields': (
                'early_bird_price',
                'early_start',
                'early_end',
            ),
            'classes': ('collapse',)
        }),

        ("Regular Ticket (Late Bird)", {
            'fields': (
                'late_bird_price',
                'late_start',
                'late_end',
            ),
            'classes': ('collapse',)
        }),

        ("VIP / VVIP Fixed Price", {
            'fields': ('price','price_currency'),
            'classes': ('collapse',)
        }),

        ("Live Status", {
            'fields': ('display_current_price', 'display_phase')
        }),

    )

    def display_current_price(self, obj):
        price = obj.current_price()
        if price:
            return f"₦{price}"
        return "Not Active"
    display_current_price.short_description = "Current Price"

    def display_phase(self, obj):
        return obj.phase()
    display_phase.short_description = "Current Phase"



@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("currency", "bank_name", "account_number", "account_name", "is_active")


@admin.register(TicketPurchase)
class TicketPurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "ticket",
        "currency",
        "is_paid",
        "created_at"
    )

    list_filter = ("is_paid", "currency")

    actions = ["verify_payment"]


    def verify_payment(self, request, queryset):

        queryset.update(is_paid=True)
