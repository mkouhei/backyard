"""backyard.inventory.admin."""
from django.contrib import admin
from backyard.inventory.models import (Maker,
                                       Product,
                                       ExternalAccount,
                                       Shop,
                                       PriceHistory,
                                       Inventory,
                                       OrderHistory,
                                       ReceiveHistory,
                                       UnpackHistory)
from backyard.inventory.queryset.inventory import QuantityQuerySet
from backyard.inventory.queryset.order_history import OrderQuerySet


class MakerAdmin(admin.ModelAdmin):
    """customize Maker list view."""
    list_display = ('name',)


class ProductAdmin(admin.ModelAdmin):
    """customize Product list view."""
    list_display = ('name', 'maker_name')

    def maker_name(self, obj):
        """maker name."""
        return obj.maker.name


class ExternalAccountAdmin(admin.ModelAdmin):
    """customize External account list view."""
    list_display = ('name', 'email', 'password_configured')

    def password_configured(self, obj):
        """password configured."""
        return obj.encrypted_password is not None


class ShopAdmin(admin.ModelAdmin):
    """customize Shop list view."""
    list_display = ('name', 'url', 'user_name')

    def user_name(self, obj):
        """user name."""
        return obj.user.name


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


class InventoryAdmin(admin.ModelAdmin):
    """Inventories list view."""
    list_display = ('product_name',
                    'ordered',
                    'received',
                    'unpacked',
                    'remain')

    def product_name(self, obj):
        """product name."""
        return obj.product.name

    def ordered(self, obj):
        """ordred quantity."""
        return QuantityQuerySet(obj).ordered_quantity()

    def received(self, obj):
        """received quantity."""
        return QuantityQuerySet(obj).received_quantity()

    def unpacked(self, obj):
        """unpacked quantity."""
        return QuantityQuerySet(obj).unpacked_quantity()

    def remain(self, obj):
        """remain quantity."""
        return QuantityQuerySet(obj).remain_quantity()


class OrderHistoryAdmin(admin.ModelAdmin):
    """Order histories list view."""
    list_display = ('ordered_at',
                    'ordered_product',
                    'product_price',
                    'quantity',
                    'amount',
                    'created_at')

    def ordered_product(self, obj):
        """order item name."""
        return OrderQuerySet(obj).ordered_product()

    def product_price(self, obj):
        """product price."""
        return OrderQuerySet(obj).product_price()

    def amount(self, obj):
        """amount."""
        return OrderQuerySet(obj).amount()


class ReceiveHistoryAdmin(admin.ModelAdmin):
    """receive histories."""
    list_display = ('received_at', 'received_item', 'quantity')


class UnpackHistoryAdmin(admin.ModelAdmin):
    """unpacked histories."""
    list_display = ('unpacked_at', 'unpacked_item', 'quantity')


admin.site.register(Maker, MakerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ExternalAccount, ExternalAccountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(ReceiveHistory, ReceiveHistoryAdmin)
admin.site.register(UnpackHistory, UnpackHistoryAdmin)
