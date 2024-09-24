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
from .form import NewsletterForm
from django.contrib import admin
from django.contrib import messages
from django.conf import settings
from .models import EmailSubscription
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
import datetime
from django.shortcuts import redirect


def send_newsletter(modeladmin, request, queryset):
    email_list = [subscriber.email for subscriber in queryset]
    
    # Initialize form with POST data if present, otherwise create an empty form
    form = NewsletterForm(request.POST or None)
    
    if 'apply' in request.POST:  # Check if the form was submitted
        if form.is_valid():
            print("Form is valid")  # Debug: Ensure this is printed      
            subject = form.cleaned_data['subject']
            heading = form.cleaned_data['heading']
            message = form.cleaned_data['message']
            url = form.cleaned_data['url']
            
            if email_list:
                try:
                    print("Preparing email...")  # Debug message

                    # Context for the email template
                    context = {
                        'heading': heading,
                        'subject': subject,
                        'message': message,
                        'url': url if url else 'https://yourwebsite.com/newsletter',  # Optional default URL
                        'year': datetime.datetime.now().year,
                    }

                    # Render the HTML template
                    html_content = render_to_string('emails/newsletter_email.html', context)
                    text_content = strip_tags(html_content)

                    # Create an email message
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=email_list,
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=False)

                    print("Email sent")  # Debug message

                    messages.success(request, f'Successfully sent emails to {len(email_list)} subscribers.')
                except Exception as e:
                    print(f"Error: {e}")  # Debug the error
                    messages.error(request, f'An error occurred: {e}')
                else:
                    messages.error(request, 'No subscribers selected.')
                return redirect(request.get_full_path())

    # If the form wasn't submitted or wasn't valid, render the form
    return render(request, 'admin/newsletter_form.html', {'form': form, 'subscribers': queryset})


# Customize the EmailSubscriptionAdmin to include the action
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')  # Customize the list display as needed
    actions = [send_newsletter]  # Add the send_newsletter function as an action

# Register the model with the custom admin class
admin.site.register(EmailSubscription, EmailSubscriptionAdmin)



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
    list_display = ['user', 'items', 'item_price_display', 'delivery_fee_display', 'total_price_display', 'reference', 'is_ordered', 'is_delivered', 'is_received', 'is_refund_request', 'refund_granted', 'view_invoice_button', 'download_invoice_button', 'send_invoice_button', 'approve_order_button','cancel_order_button']
    # list_display = ['user', 'items', 'total_price_display', 'reference', 'is_ordered', 'is_delivered', 'is_received', 'is_refund_request', 'refund_granted', 'view_invoice_button', 'download_invoice_button', 'send_invoice_button', 'approve_order_button','cancel_order_button']
    readonly_fields = ('user',)
    list_filter = ['is_ordered','is_delivered', 'is_received', 'is_refund_request']
    list_display_links = ['user','items',]
    search_fields = ['user__username', 'reference']
    
    
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.filter(is_ordered=True)
    
    
    @admin.display(description='Item(s) Price')
    def item_price_display(self, obj):
        total_price_value = obj.get_total()
        formatted_price = "₦{:,.2f}".format(float(total_price_value))
        return format_html('<p class="h5">{}</p>', formatted_price)
    
    @admin.display(description='Delivery Fee')
    def delivery_fee_display(self, obj):
        delivery_cost_value = obj.get_delivery_cost()
        formatted_price = "₦{:,.2f}".format(float(delivery_cost_value))
        return format_html('<p class="h5">{}</p>', formatted_price)
    
    @admin.display(description='Total')
    def total_price_display(self, obj):
        total_price_value = obj.get_total_with_delivery()
        formatted_price = "₦{:,.2f}".format(float(total_price_value))
        return format_html('<p class="h5">{}</p>', formatted_price)
    
    # Add buttons to view, download, and send the invoice
    @admin.display(description='Invoice Action')
    def view_invoice_button(self, obj):
        return format_html('<a class="btn btn-light" href="{}">View Invoice</a>', reverse('admin:view_invoice', args=[obj.id]))

    @admin.display(description='Download Invoice')
    def download_invoice_button(self, obj):
        return format_html('<a class="btn btn-light" href="{}">Download Invoice</a>', reverse('admin:download_invoice', args=[obj.id]))

    @admin.display(description='Send Invoice')
    def send_invoice_button(self, obj):
        return format_html('<a class="btn btn-secondary" href="{}">Send Invoice</a>', reverse('admin:send_invoice', args=[obj.id]))
    
    @admin.display(description='Cancel Order')
    def cancel_order_button(self, obj):
        if not obj.approved:  # Show cancel button only if the order is not already approved
            return format_html(
                '<a class="btn btn-danger" href="{}">Cancel Order</a>', 
                reverse('admin:cancel_order', args=[obj.id])
            )
        return ''


    # Add buttons to view, download, send invoice and approve order
    @admin.display(description='Approve Order')
    def approve_order_button(self, obj):
        if not obj.approved:  # Only show button if the order is not already approved
            return format_html('<a class="btn btn-success" href="{}">Approve Order</a>', reverse('admin:approve_order', args=[obj.id]))
        return format_html('<buttton class="btn btn-success">Approved</>')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/view-invoice/', self.admin_site.admin_view(self.view_invoice), name='view_invoice'),
            path('<int:order_id>/send-invoice/', self.admin_site.admin_view(self.send_invoice), name='send_invoice'),
            path('<int:order_id>/download-invoice/', self.admin_site.admin_view(self.download_invoice), name='download_invoice'),
            path('<int:order_id>/cancel-order/', self.admin_site.admin_view(self.cancel_order), name='cancel_order'),
            path('<int:order_id>/approve-order/', self.admin_site.admin_view(self.approve_order), name='approve_order'),
           
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
    

    def approve_order(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            # Fetch delivery location based on the order (assuming `delivery_location` field exists in the Order model)
            delivery_location = DeliveryLocations.objects.get(state=order.delivery_location.state, town_name=order.delivery_location.town_name)
            delivery_days = delivery_location.delivery_days

            # Update order status to approved
            order.approved = True
            order.save()

            # Send email to user
            subject = f'Order Approved - Reference {order.reference}'
            message = render_to_string('emails/order_approved_email.html', {
                'order': order,
                'delivery_days': delivery_days,
            })
            email = EmailMessage(
                subject,
                message,
                to=[order.user.email]
            )
            email.content_subtype = 'html'
            email.send()

            # Admin feedback message
            self.message_user(request, f"Order {order.reference} approved successfully and email sent to user.")
        except Order.DoesNotExist:
            self.message_user(request, "Order does not exist.", level=messages.ERROR)
        except DeliveryLocations.DoesNotExist:
            self.message_user(request, "Delivery location not found for the order.", level=messages.ERROR)
        except Exception as e:
            self.message_user(request, f"Error approving order: {e}", level=messages.ERROR)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    def cancel_order(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            if order.approved:
                self.message_user(request, "Cannot cancel an approved order.", level=messages.ERROR)
            else:
                # Cancel the order
                order.is_ordered = False  # Or set a `canceled` field if it exists
                order.save()

                # Send email notification to the user
                subject = f'Order Canceled - Reference {order.reference}'
                message = render_to_string('emails/cancel_order_email.html', {
                    'order': order,
                })
                email = EmailMessage(
                    subject,
                    message,
                    to=[order.user.email]
                )
                email.content_subtype = 'html'
                email.send()

                self.message_user(request, f"Order {order.reference} canceled and email sent to the user.")
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
    list_display = ['user', 'street_address', 'apartment', 'town', 'state', 'zip_code', 'telephone']



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