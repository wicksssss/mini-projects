from django.contrib import admin
from .models import Category, Brand, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


def deactivate_products(modeladmin, request, queryset):
    queryset.update(is_active=False)


deactivate_products.short_description = 'Deactivate selected products'


def apply_discount_10(modeladmin, request, queryset):
    for product in queryset:
        product.discount_price = round(product.price * 0.9, 2)
        product.save()


apply_discount_10.short_description = 'Apply 10 percent discount'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active')
    list_filter = ('category', 'brand', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    actions = [deactivate_products, apply_discount_10]
