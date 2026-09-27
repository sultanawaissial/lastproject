"""
URL configuration for lastproject project.
"""
from django.contrib import admin
from django.urls import path, include
from lastapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Django default admin
    path('admin/', admin.site.urls),

    # --- Public Pages ---
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/<str:category>/', views.shop_view, name='shop-category'), # ab /shop/men-steel/ /shop/all/ sab isi se handle hoga
    path('products/', views.products_view, name='products'), # agar ye alag page hai to rehne do, warna hata do
    
    # --- User Account ---
    path('my-account/', views.profile_view, name='my_account'),
    path('profile/', views.profile_view, name='profile'), # purana link kharab na ho is liye rakha hai, redirect kar dega

    # --- Auth (Login/Logout ke liye zaroori) ---
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # --- Custom Admin Dashboard jo tumne banaya hai ---
    path('my-admin/', views.my_admin_dashboard, name='my_admin'),

    # --- Cart / Wishlist / Orders ke liye future URLs ---
    # path('cart/', views.cart_view, name='cart'),
    # path('wishlist/', views.wishlist_view, name='wishlist'),
]

# Media files ke liye (carousel, products, logo images ke liye LAZMI hai)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 404 Handler (optional)
handler404 = 'lastapp.views.custom_404_view'