from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from book_store.models import Order
from delivery.models import DeliveryLocations

from twilio.rest import Client
from django.conf import settings
from book_store.models import Profile
from .deliveryform import PhoneNumberForm, OTPForm
from django.shortcuts import redirect, render
from twilio.rest import Client
# from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from aa_jomos import settings
from twilio.base.exceptions import TwilioRestException
import re
@csrf_exempt
@require_POST
def update_delivery_cost(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
        state = request.POST.get('state')
        town = request.POST.get('town')

        try:
            order = Order.objects.get(user=request.user, is_ordered=False)
            delivery_location = DeliveryLocations.objects.get(state=state, town_name=town)
            
            # Calculate delivery cost and update the order's delivery location
            delivery_cost = delivery_location.delivery_cost
            order.delivery_location = delivery_location
            order.save()
            
            # Calculate the total with delivery
            total_with_delivery = order.get_total_with_delivery()  # Assuming you have a method for this

            response_data = {
                'success': True,
                'total_with_delivery': total_with_delivery,
                'delivery_cost': delivery_cost
            }
        except (Order.DoesNotExist, DeliveryLocations.DoesNotExist):
            response_data = {
                'success': False,
                'error': 'Invalid state or town, or no active order found.'
            }
        return JsonResponse(response_data)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})





@method_decorator(login_required, name='dispatch')
class PhoneNumberView(View):
    def get(self, request, *args, **kwargs):
        form = PhoneNumberForm()
        return render(request, 'enter_phone_number.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            # Ensure the phone number is converted to a string
            phone_number_str = str(phone_number)
            
            # Validate the phone number format (E.164)
            if not re.match(r'^\+?\d{10,15}$', phone_number_str):
                messages.error(request, 'Invalid phone number format. Please enter a valid phone number.')
                return render(request, 'enter_phone_number.html', {'form': form})

            # Save the phone number to the user's profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.phone_number = phone_number
            profile.save()

            # Send OTP using Twilio
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)
                verification = client.verify \
                    .services(settings.TWILIO_VERIFICATION_SERVICE_SID) \
                    .verifications \
                    .create(to=phone_number_str, channel='sms')

                return redirect('verify_phone_number')
            except TwilioRestException as e:
                messages.error(request, f"Twilio error: {e.msg}")
                return render(request, 'enter_phone_number.html', {'form': form})

        messages.error(request, 'Please provide a valid phone number.')
        return render(request, 'enter_phone_number.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class VerifyPhoneNumberView(View):
    def get(self, request, *args, **kwargs):
        form = OTPForm()
        return render(request, 'store/verify_phone_number.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            profile = Profile.objects.get(user=request.user)
            phone_number = profile.phone_number

            # Verify OTP using Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILLO_AUTH_TOKEN)
            verification_check = client.verify \
                .services(settings.TWILO_ACCOUNT_SID) \
                .verification_checks \
                .create(to=str(phone_number), code=otp)

            if verification_check.status == 'approved':
                # Mark phone number as verified
                profile.is_phone_verified = True
                profile.save()

                messages.success(request, 'Phone number verified successfully.')
                return redirect('checkout')

            messages.error(request, 'Invalid OTP. Please try again.')
        return render(request, 'store/verify_phone_number.html', {'form': form})
