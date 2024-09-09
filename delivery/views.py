from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from book_store.models import Order
from delivery.models import DeliveryLocations
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
