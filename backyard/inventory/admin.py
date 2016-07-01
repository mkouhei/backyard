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
    list_display = ('product_name',)

    def product_name(self, obj):
        """product name."""
        return obj.product.name


class OrderHistoryAdmin(admin.ModelAdmin):
    """Order histories list view."""
    list_display = ('ordered_at',
                    'order_item_name',
                    'product_price',
                    'count',
                    'amount',
                    'created_at')

    def order_item_name(self, obj):
        """order item name."""
        return obj.order_item.product

    def product_price(self, obj):
        """product price."""
        return obj.order_item.price

    def amount(self, obj):
        """amount."""
        return obj.amount()


class ReceiveHistoryAdmin(admin.ModelAdmin):
    """receive histories."""
    list_display = ('received_at', 'received_item', 'difference_count')


class UnpackHistoryAdmin(admin.ModelAdmin):
    """unpacked histories."""
    list_display = ('unpacked_at', 'unpacked_item', 'count')


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount')


admin.site.register(Maker, MakerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ExternalAccount, ExternalAccountAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(PriceHistory, PriceHistoryAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(ReceiveHistory, ReceiveHistoryAdmin)
admin.site.register(UnpackHistory, UnpackHistoryAdmin)
