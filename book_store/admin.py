from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from.models import *
from .models  import  Payment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import path
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Order
from xhtml2pdf import pisa
import io
from  django.shortcuts import get_object_or_404

# class SendInvoiceView(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('send-invoice/<int:order_id>/', self.admin_site.admin_view(self.send_invoice), name='send_invoice'),
#         ]
#         return custom_urls + urls

#     def send_invoice(self, request, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
#             subject = f'Invoice for Order {order.id}'
#             message = render_to_string('invoice_template.html', {'order': order})
#             email = EmailMessage(subject, message, 'your-email@example.com', [order.customer.email])
#             email.content_subtype = 'html'
#             email.send()

#             self.message_user(request, f"Invoice for order {order.id} sent successfully.")
#         except Order.DoesNotExist:
#             self.message_user(request, "Order does not exist.", level=messages.ERROR)
#         except Exception as e:
#             self.message_user(request, f"Error sending invoice: {e}", level=messages.ERROR)

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'shipping_address', 'total_price', 'reference', 'is_ordered', 'is_delivered', 'is_received', 'is_refund_request', 'refund_granted', 'view_invoice_button', 'download_invoice_button']
    readonly_fields = ('user',)
    list_filter = ['is_ordered','is_delivered', 'is_received', 'is_refund_request']
    list_display_links = ['user','items', 'shipping_address']
    search_fields = ['user__username', 'reference']

    # Add buttons to view and download the invoice
    def view_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">View Invoice</a>', reverse('admin:view_invoice', args=[obj.id]))
    view_invoice_button.short_description = 'Invoice Action'
    
    def download_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">Download Invoice</a>', reverse('admin:download_invoice', args=[obj.id]))
    download_invoice_button.short_description = 'Download Invoice'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/view-invoice/', self.admin_site.admin_view(self.view_invoice), name='view_invoice'),
            path('<int:order_id>/send-invoice/', self.admin_site.admin_view(self.send_invoice), name='send_invoice'),
            path('<int:order_id>/download-invoice/', self.admin_site.admin_view(self.download_invoice), name='download_invoice'),
        ]
        return custom_urls + urls

    # Render the invoice in HTML format
    def view_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            # Check if the invoice exists for the order
            try:
                invoice = get_object_or_404(Invoice, order=order)
            except Invoice.DoesNotExist:
                self.message_user(request, "Invoice does not exist for this order.", level=messages.ERROR)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            context = {'order': order, 'invoice': invoice}
            return render(request, 'store/invoice.html', context)
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Send the invoice via email
    def send_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            subject = f'Invoice for Order {order.id}'
            message = render_to_string('store/invoice.html', {'order': order})
            email = EmailMessage(subject, message, 'andrewsamuelcloud@gmail.com', [order.user.email])
            email.content_subtype = 'html'
            email.send()

            self.message_user(request, f"Invoice for order {order.id} sent successfully.")
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error sending invoice: {e}", level=messages.ERROR)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Download the invoice as a PDF
    def download_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            context = {'order': order}
            html = render_to_string('store/invoice.html', context)

            # Generate PDF from HTML
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="invoice_{order.reference}.pdf"'

            result = io.BytesIO()
            pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=result)

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')

            response.write(result.getvalue())
            return response
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ["user","ref",'amount', "verified", "date_created"]

admin.site.register(Payment, PaymentAdmin)


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img_1.url))
    list_display = ['title', 'image_tag',]
    image_tag.short_description = 'Image'
    

class CartAdmin(admin.ModelAdmin):    
    list_display = ['product', 'user', 'get_price_tag', 'cart_id'] 
    class Meta:
        Model= Cart
                    

class make_accept_refund(admin.ModelAdmin, ):
    autocomplete_fields = ['is_refund_request', 'refund_granted']


make_accept_refund.short_description = 'update refund granted'
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'shipping_address', 'total_price', 'reference', 'is_ordered', 'is_delivered', 'is_received', 'is_refund_request', 'refund_granted', 'view_invoice_button']
    readonly_fields = ('user',)
    list_filter = ['is_ordered','is_delivered', 'is_received', 'is_refund_request']
    list_display_links = ['user','items', 'shipping_address']
    search_fields = ['user__username', 'reference']

    # Add a custom button to view the invoice in the admin panel
    def view_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">View Invoice</a>', reverse('admin:view_invoice', args=[obj.id]))
    view_invoice_button.short_description = 'Invoice Action'
    view_invoice_button.allow_tags = True

    # Define custom URLs for viewing and sending the invoice
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/view-invoice/', self.admin_site.admin_view(self.view_invoice), name='view_invoice'),
            path('<int:order_id>/send-invoice/', self.admin_site.admin_view(self.send_invoice), name='send_invoice'),
        ]
        return custom_urls + urls

    # Custom action to view the invoice
    def view_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            # Render the invoice template with order context
            context = {'order': order}
            return render(request, 'store/invoice.html', context)
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Custom action to send the invoice via email
    def send_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            subject = f'Invoice for Order {order.id}'
            message = render_to_string('invoice_template.html', {'order': order})
            email = EmailMessage(subject, message, 'your-email@example.com', [order.user.email])
            email.content_subtype = 'html'
            email.send()

            self.message_user(request, f"Invoice for order {order.id} sent successfully.")
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error sending invoice: {e}", level=messages.ERROR)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



admin.site.register(Order, OrderAdmin)
 
    
    
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
admin.site.register(Category, CategoryAdmin)

admin.site.register(CustomersAddress, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refunds)
admin.site.register(Color)
admin.site.register(ProductSizeColor)

admin.site.register(Inventory, InventAdmin)

admin.site.register(Size)
admin.site.register(Stock)
admin.site.register(Invoice)
admin.site.register(AbujaLocation)
admin.site.register(Wishlist)
actions = [make_accept_refund]