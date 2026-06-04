from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Order, OrderItem
from accounts.models import UserProfile


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__email',)
    inlines = [OrderItemInline]

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Позначити як відправлено'

    actions = ['mark_as_shipped']


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.site_header = 'BeautyShop Адмінпанель'
admin.site.site_title = 'BeautyShop'
