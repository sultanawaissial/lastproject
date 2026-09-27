# lastapp/context_processors.py - FINAL CLEAN VERSION

from .models import Settings, NavbarItem, FooterColumn

def site_settings(request):
    # Tumhare model me get_settings() method hai, usi ko use karenge
    # .first() se agar DB me 2 settings ban gaye to kabhi kabhi galat wala uth jayega
    
    try:
        settings_obj = Settings.get_settings()
    except Exception:
        settings_obj = None

    # Header / Footer dynamic items
    # is_active check lazmi hai warna admin ne off kiya hua item bhi dikhega
    try:
        nav_items = NavbarItem.objects.filter(is_active=True).order_by('order')
        footer_columns = FooterColumn.objects.prefetch_related('links').order_by('order')
    except Exception:
        nav_items = []
        footer_columns = []

    return {
        'site_settings': settings_obj, # tumhara purana naam same rakha hai taake templates na toote
        'settings_obj': settings_obj,   # new naam bhi de diya
        'nav_items': nav_items,
        'footer_columns': footer_columns,
        'site_navbar': nav_items, # alias
    }