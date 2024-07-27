from django.contrib import admin
from django.utils.html import format_html
from.models import *
from .models  import  Payment

class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ["user","ref",'amount', "verified", "date_created"]

admin.site.register(Payment, PaymentAdmin)


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img_1.url))
    list_display = ['title', 'image_tag', 'price', 'discount_price']
    image_tag.short_description = 'Image'
    

class CartAdmin(admin.ModelAdmin):    
    list_display = ['product', 'user', 'get_price_tag', 'cart_id'] 
    class Meta:
        Model= Cart
                    

class make_accept_refund(admin.ModelAdmin, ):
    autocomplete_fields = ['is_refund_request', 'refund_granted']


make_accept_refund.short_description = 'update refund granted'
    

class OrderAdmin(admin.ModelAdmin):
    list_display= [ 'user','items','shipping_address','total_price','reference','is_ordered','is_delivered', 'is_received', 'is_refund_request', 'refund_granted']
    readonly_fields = ('user',)
    list_filter =  [ 'is_ordered','is_delivered', 'is_received', 'is_refund_request', ]
    
    list_display_links = ['user','items', 'shipping_address']
    search_fields = ['user__username', 'reference']
    
    
    
class CategoryAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img.url))
    list_display = ['title', 'image_tag']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['__all__']


class CouponAdmin(admin.ModelAdmin):
        list_display = ['code', 'valid_from', 'valid_to','active','user','is_used']

        list_filter = ['active', 'valid_from', 'valid_to']

        search_fields = ['code']

class InventAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'apartment', 'town', 'zip_code', 'telephone']



admin.site.register(Product, ProductAdmin) 
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(CustomersAddress, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refunds)
admin.site.register(Features)
# admin.site.register(CustomerRating)

admin.site.register(Inventory, InventAdmin)

admin.site.register(Size)
admin.site.register(Stock)
admin.site.register(Invoice)
admin.site.register(AbujaLocation)
admin.site.register(Wishlist)
actions = [make_accept_refund]