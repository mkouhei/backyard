"""backyard.inventory.admin."""
from django.contrib import admin

from .models.maker import Maker
from .models.product import Product
from .models.external_account import ExternalAccount
from .models.shop import Shop
from .models.price_history import PriceHistory
from .models.order_history import OrderHistory
from .models.unpack_history import UnpackHistory
from .queryset.product import ProductQuerySet


class MakerAdmin(admin.ModelAdmin):
    """customize Maker list view."""
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    """customize Product list view."""
    list_display = ('name', 'maker_name', 'ordered', 'received', 'unpacked', 'remain')

    def maker_name(self, obj):
        """maker name."""
        return obj.maker.name

    def ordered(self, obj):
        """ordered quantity."""
        return ProductQuerySet(obj).ordered_quantity

    def received(self, obj):
        """received quantity."""
        return ProductQuerySet(obj).received_quantity

    def unpacked(self, obj):
        """unpacked quantity."""
        return ProductQuerySet(obj).unpacked_quantity

    def remain(self, obj):
        """remain quantity."""
        return ProductQuerySet(obj).remain_quantity


class ExternalAccountAdmin(admin.ModelAdmin):
    """customize External account list view."""
    list_display = ('name', 'email', 'password_configured')

    def password_configured(self, obj):
        """password configured."""
        return obj.encrypted_password is not None


class ShopAdmin(admin.ModelAdmin):
    """customize Shop list view."""
    list_display = ('name', 'url')


class PriceHistoryAdmin(admin.ModelAdmin):
    """customize Price hitories list view."""
    list_display = ('registered_date',
                    'product_name',
                    'shop_name',
                    'price',
                    'currency_unit',
                    'created_at')

    def product_name(self, obj):
        """product name."""
        return obj.product.name

    def shop_name(self, obj):
        """Shop name."""
        return obj.shop.name


class OrderHistoryAdmin(admin.ModelAdmin):
    """Order histories list view."""
    list_display = ('ordered_at',
                    'product',
                    'group',
                    'price',
                    'ordered_quantity',
                    'amount',
                    'received_at',
                    'received_quantity',
                    'created_at')

    def amount(self, obj):
        """amount."""
        return obj.ordered_quantity * obj.price.price


class UnpackHistoryAdmin(admin.ModelAdmin):
    """unpacked histories."""
    list_display = ('unpacked_at',
                    'product',
                    'group',
                    'quantity')


admin.site.register(Maker, MakerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ExternalAccount, ExternalAccountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(UnpackHistory, UnpackHistoryAdmin)
