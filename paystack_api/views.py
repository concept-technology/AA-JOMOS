from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
import requests

from aa_jomos import settings
from book_store.models import Cart, CustomersAddress, Invoice, Order, Payment
from book_store.views import create_ref_code, generate_random_number

# Create your views here.

def initiate_payment(request):
    order = Order.objects.get(is_ordered=False, user=request.user)
    cart = Cart.objects.filter(user=request.user, is_ordered=False)

    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        pk = settings.PAYSTACK_PUBLIC_KEY

        # Convert amount to float instead of int
        payment = Payment.objects.create(amount=float(amount), email=email, order=order, user=request.user)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
            'order': order,
            'cart':cart,       
        }
        
        return render(request, 'store/make-payment.html', context)

    return render(request, 'store/payment.html', {'order': order, 'cart': cart})


def verify_payment(request, ref):
    try:
        order = Order.objects.get(is_ordered=False, user=request.user)
        payment = Payment.objects.get(ref=ref)
        address = CustomersAddress.objects.get(user=request.user)
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY
        verify_url = f'https://api.paystack.co/transaction/verify/{ref}'
        headers = {
            'Authorization': f'Bearer {paystack_secret_key}',
            'Content-Type': 'application/json',
        }
        response = requests.get(verify_url, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            paystack_amount = data['data']['amount'] / 100  # Convert kobo to naira
            expected_amount = order.get_total_with_delivery()

            if paystack_amount == expected_amount and data['data']['status'] == 'success':
                payment.verified = True
                payment.save()
                # Mark order products as ordered
                order_products = order.product.all()
                order_products.update(is_ordered=True)

                # Update order status and create invoice
                order.is_ordered = True
                order.payment = payment
                order.reference = create_ref_code() #create a reference code
                order.save()

                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=generate_random_number(),  # function for generating invoice numbers
                    order=order,
                    payment=payment,
                    issued_at = timezone.datetime.now()
                    # Add more fields as needed
                )
                invoice.save()
                # save additional invoice details
                order.invoice_number =  invoice.invoice_number
                order.save()
                order.shipping_address =address
                return render(request,'store/success.html', {'invoice': invoice, 'order': order, 'payment': payment})
            else:
                return render(request, 'store/payment_not_successful.html')

        else:
            print(f"Failed to verify payment. Status code: {response.status_code}, Paystack response: {response.text}")
            return JsonResponse({'status': 'error', 'message': 'Failed to verify payment.'})

    except Order.DoesNotExist:
        print("Order does not exist for the user.")
        return JsonResponse({'status': 'error', 'message': 'Order does not exist for the user.'})
    except Payment.DoesNotExist:
        print("Payment does not exist for the reference.")
        return JsonResponse({'status': 'error', 'message': 'Payment does not exist for the reference.'})
    except requests.exceptions.RequestException as e:
        print(f"Error verifying payment: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f"Error verifying payment: {str(e)}"})

