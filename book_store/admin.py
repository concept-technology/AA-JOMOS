from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from prompt_toolkit import HTML
from.models import *
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
# from weasyprint import HTML
from io import BytesIO
from pdf2image import convert_from_path




class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img_1.url))
    list_display = ['title', 'image_tag', 'total_stock']
    image_tag.short_description = 'Image'
    

class CartAdmin(admin.ModelAdmin):    
    list_display = ['product', 'user', 'get_price_tag', 'cart_id'] 
    class Meta:
        Model= Cart
                    

class make_accept_refund(admin.ModelAdmin, ):
    autocomplete_fields = ['is_refund_request', 'refund_granted']


make_accept_refund.short_description = 'update refund granted'
# order admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'shipping_address', 'total_price', 'reference', 'is_ordered', 'is_delivered', 'is_received', 'is_refund_request', 'refund_granted', 'view_invoice_button', 'download_invoice_button', 'send_invoice_button']
    readonly_fields = ('user',)
    list_filter = ['is_ordered','is_delivered', 'is_received', 'is_refund_request']
    list_display_links = ['user','items', 'shipping_address']
    search_fields = ['user__username', 'reference']

    # Add buttons to view, download, and send the invoice
    @admin.display(description='Invoice Action')
    def view_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">View Invoice</a>', reverse('admin:view_invoice', args=[obj.id]))

    @admin.display(description='Download Invoice')
    def download_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">Download Invoice</a>', reverse('admin:download_invoice', args=[obj.id]))

    @admin.display(description='Send Invoice')
    def send_invoice_button(self, obj):
        return format_html('<a class="button" href="{}">Send Invoice</a>', reverse('admin:send_invoice', args=[obj.id]))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/view-invoice/', self.admin_site.admin_view(self.view_invoice), name='view_invoice'),
            path('<int:order_id>/send-invoice/', self.admin_site.admin_view(self.send_invoice), name='send_invoice'),
            path('<int:order_id>/download-invoice/', self.admin_site.admin_view(self.download_invoice), name='download_invoice'),
        ]
        return custom_urls + urls

    def view_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            invoice = get_object_or_404(Invoice, order=order)
            context = {
                'order': order,
                'invoice': invoice,
                'items': order.product.all(),  # Assuming items is a related name or reverse relation to the order
            }
            return render(request, 'store/invoice_template.html', context)
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    

    def send_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            invoice = get_object_or_404(Invoice, order=order)
            subject = f'Invoice for Order {order.reference}'
            message = render_to_string('store/send_invoice.html', {'order': order, 'invoice':invoice})      
            email = EmailMessage(
                subject,
                message,
                to=[order.user.email]  # No need to specify 'from_email'
            )
            
            email.content_subtype = 'html'
            email.send()
            self.message_user(request, f"Invoice for order {order.reference} sent successfully.")
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error sending invoice: {e}", level=messages.ERROR)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    
    # Download the invoice as a PDF
    def download_invoice(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            invoice = get_object_or_404(Invoice, order=order)
            context = {'order': order,'invoice':invoice}
            html = render_to_string('store/invoice_template.html', context)
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
    
    
    # generated invoice in pdf format
    def generate_invoice_pdf(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        context = {
            'order': order,
            'invoice_number': f"INV-{order_id:08d}",
        }

        # Render the invoice HTML template
        html_string = render_to_string('store/invoice_template.html', context)
        html = HTML(string=html_string)
        
        # Generate PDF
        pdf_file = html.write_pdf()
        
        # Create HTTP response with PDF file
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'
        
        return response


    def generate_invoice_image(order_id):
        # Generate PDF as before
        pdf = generate_invoice_pdf(order_id)
        
        # Convert PDF to image
        images = convert_from_path(BytesIO(pdf), dpi=300)  # Converts PDF to images

        # Save image
        image_path = f'/path/to/save/invoice_{order_id}.png'
        images[0].save(image_path, 'PNG')
        
        return image_path


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

admin.site.register(Wishlist)
actions = [make_accept_refund]