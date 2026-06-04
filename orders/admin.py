from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


def mark_as_shipped(modeladmin, request, queryset):
    queryset.update(status='shipped')
mark_as_shipped.short_description = 'Mark as shipped'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__email',)
    inlines = [OrderItemInline]
    actions = [mark_as_shipped]