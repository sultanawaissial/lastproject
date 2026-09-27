# lastapp/models.py - FINAL PRODUCTION VERSION
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import uuid

# ================= SETTINGS =================
class Settings(models.Model):
    site_name = models.CharField(max_length=100, default="Vantico")
    site_meta_title = models.CharField(max_length=100, blank=True)
    site_description = models.TextField(blank=True)
    site_keywords = models.CharField(max_length=255, blank=True, null=True)
    site_tagline = models.CharField(max_length=255, blank=True, null=True)
    site_url = models.URLField(default="https://example.com")
    site_author = models.CharField(max_length=100, blank=True, null=True)

    site_logo = models.ImageField(upload_to='site_logo/', blank=True, null=True)
    site_logo_dark = models.ImageField(upload_to='site_logo/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='site_favicon/', blank=True, null=True)
    site_og_image = models.ImageField(upload_to='site_seo/', blank=True, null=True)
    site_theme_color = models.CharField(max_length=7, default="#000000")

    site_email = models.EmailField(blank=True, null=True)
    site_phone = models.CharField(max_length=20, blank=True, null=True)
    site_whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    site_address = models.TextField(blank=True, null=True)
    site_map_embed = models.TextField(blank=True, null=True)
    site_business_hours = models.CharField(max_length=255, blank=True, null=True)

    site_language = models.CharField(max_length=50, default="en")
    site_currency = models.CharField(max_length=10, default="PKR")
    site_currency_symbol = models.CharField(max_length=5, default="Rs.")
    site_timezone = models.CharField(max_length=50, default="Asia/Karachi")
    site_pagination_count = models.PositiveIntegerField(default=12)

    site_social_links = models.JSONField(default=dict, blank=True)
    site_google_analytics_id = models.CharField(max_length=100, blank=True, null=True)
    site_google_tag_manager_id = models.CharField(max_length=100, blank=True, null=True)
    site_facebook_pixel_id = models.CharField(max_length=100, blank=True, null=True)
    site_google_search_console = models.CharField(max_length=255, blank=True, null=True)
    site_robots_txt = models.TextField(blank=True, null=True, default="User-agent: *\nAllow: /\n")
    site_header_script = models.TextField(blank=True, null=True)
    site_footer_script = models.TextField(blank=True, null=True)
    site_custom_css = models.TextField(blank=True, null=True)
    site_custom_js = models.TextField(blank=True, null=True)
    site_chatbot_code = models.TextField(blank=True, null=True)

    # Spelling fixed + purani spelling ko property se handle kiya
    site_announcement_text = models.TextField(blank=True, null=True)
    site_announcement_link = models.URLField(blank=True, null=True)
    site_announcement_status = models.BooleanField(default=False)

    site_maintenance_mode = models.BooleanField(default=False)
    site_maintenance_message = models.TextField(blank=True, null=True, default="We are under maintenance.")

    site_footer_text = models.TextField(blank=True, null=True)
    site_copyright_text = models.TextField(default="© 2026 All Rights Reserved.")

    site_enable_registration = models.BooleanField(default=True)
    site_enable_blog = models.BooleanField(default=True)
    site_enable_shop = models.BooleanField(default=False)
    
    site_recaptcha_site_key = models.CharField(max_length=255, blank=True, null=True)
    site_recaptcha_secret_key = models.CharField(max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# ================= PRODUCT =================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men_steel', 'Men Steel'),
        ('women_steel', 'Women Steel'),
        ('smart', 'Smart Watches'),
        ('couple', 'Couple Watches'),
    ]
    
    name = models.CharField(max_length=100)
    # CharField rakha hai taake tumhara purana data kharab na ho
    categories = models.CharField(max_length=100, help_text="e.g: men steel, women steel, smart")
    product_type = models.CharField(max_length=100, default="Men's Stainless Steel")
    
    # FIX: Image field add kiya
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(blank=True, null=True)
    discount_percent = models.PositiveIntegerField(blank=True, null=True, help_text="e.g: 20 for 20%")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("4.7"))
    icon_name = models.CharField(max_length=50, default="watch", help_text="bootstrap icon name without bi-")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_discount(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return self.discount_percent or 0

# ================= USER PROFILE =================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

# ================= ORDERS & WISHLIST =================
class Order(models.Model):
    STATUS_CHOICES = [('Pending','Pending'),('Processing','Processing'),('Delivered','Delivered'),('Cancelled','Cancelled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    product_name = models.CharField(max_length=200)
    # FIX: Product se link bhi rakho
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # Ek product ek dafa hi wishlist me
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# ================= CAROUSEL & NAVBAR (Purane wale - naam change nahi kiya) =================
class carousel(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.CharField(max_length=200)
    def __str__(self):
        return self.caption

class navbar(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    def __str__(self):
        return self.name

# ================= NEW DYNAMIC HEADER/FOOTER =================
class NavbarItem(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.name

class FooterColumn(models.Model):
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title

class FooterLink(models.Model):
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.column.title} - {self.name}"