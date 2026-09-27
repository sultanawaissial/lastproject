# lastapp/views.py - FINAL CLEAN VERSION

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator

from .models import Product, carousel, Settings, Order, Wishlist, Profile, NavbarItem, FooterColumn

# Helper: Har page pe Settings chahiye hoga
def get_common_context():
    return {
        'settings_obj': Settings.get_settings(),
        'nav_items': NavbarItem.objects.filter(is_active=True),
        'footer_columns': FooterColumn.objects.prefetch_related('links').all(),
    }

@staff_member_required
def my_admin_dashboard(request):
    stats = {
        'products': Product.objects.count(),
        'orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='Pending').count(),
        'delivered_orders': Order.objects.filter(status='Delivered').count(),
        'revenue': Order.objects.filter(status='Delivered').aggregate(total=Sum('total_price'))['total'] or 0,
        'total_revenue_all': Order.objects.aggregate(total=Sum('total_price'))['total'] or 0,
    }
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:8]
    
    context = {**get_common_context(), **stats, 'recent_orders': recent_orders}
    return render(request, 'my_admin/dashboard.html', context)

def home_view(request):
    carousels = carousel.objects.all()
    
    # Flash Deals = jinka old_price ho aur new price kam ho
    flash_deals = Product.objects.filter(is_active=True, old_price__isnull=False).order_by('-created_at')[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    # Best Sellers = for now latest, baad me orders se count karenge
    best_sellers = Product.objects.filter(is_active=True).order_by('-id')[:8]

    context = {
        **get_common_context(),
        'carousel': carousels,
        'flash_deals': flash_deals,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
    }
    return render(request, 'index.html', context)

def shop_view(request, category='all'):
    products = Product.objects.filter(is_active=True)

    # URL se category: /shop/men-steel/ /shop/all/
    if category and category != 'all':
        products = products.filter(categories__icontains=category)

    # Search query ?q=watch
    q = request.GET.get('q')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(categories__icontains=q))

    # Category filter from dropdown ?category=smart
    cat_filter = request.GET.get('category')
    if cat_filter and cat_filter != 'all':
        products = products.filter(categories__icontains=cat_filter)

    # Pagination
    paginator = Paginator(products.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        **get_common_context(),
        'products': page_obj,
        'page_obj': page_obj,
        'current_category': category,
        'search_query': q or '',
    }
    return render(request, 'products.html', context)

def products_view(request):
    # Ab ye sirf alias hai shop_view ka, taake purane links na toote
    return shop_view(request, category=request.GET.get('category', 'all'))

@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).select_related('product').order_by('-created_at')
    wishlist = Wishlist.objects.filter(user=user).select_related('product')
    profile, created = Profile.objects.get_or_create(user=user)
    
    context = {
        **get_common_context(),
        'orders': orders,
        'wishlist': wishlist,
        'profile': profile,
        'wishlist_count': wishlist.count(),
        'orders_count': orders.count(),
    }
    return render(request, 'profile.html', context)

def custom_404_view(request, exception):
    context = get_common_context()
    return render(request, '404.html', context, status=404)