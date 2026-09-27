from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.html import format_html

from .models import (
    Product, Settings, Profile, Order, Wishlist,
    navbar, carousel,
    NavbarItem, FooterColumn, FooterLink
)

# --- CUSTOM ADMIN DASHBOARD COUNTS ---

class MyAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            'products_count': Product.objects.count(),
            'orders_count': Order.objects.count(),
            'users_count': User.objects.count(),
            'total_revenue': Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        })
        return context

# Purani site ko replace kar do
admin.site.__class__ = MyAdminSite
admin.site.index_template = 'admin/index.html'

# --- Products ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'categories', 'price', 'is_active')
    list_filter = ('categories', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_per_page = 20

# --- Settings ---
@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_email', 'site_phone')
    # Settings sirf 1 hi honi chahiye is liye add ka button hata do agar chahe to
    def has_add_permission(self, request):
        return not Settings.objects.exists()

# --- Orders ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username')
    readonly_fields = ('order_id', 'created_at')

# --- Profile & Wishlist ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

# --- Purane Models ---
@admin.register(navbar)
class AllNavbarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link')

@admin.register(carousel)
class AllCarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'caption')

    @admin.display(description='Preview')
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.image.url)
        return "No Image"

# --- Naye Dynamic Header/Footer Models ---
@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)

@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'column', 'link', 'order')
    list_filter = ('column',)
    list_editable = ('order',)