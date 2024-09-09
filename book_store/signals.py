from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, Order
import uuid

import logging
logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def transfer_cart_from_session_to_user(sender, request, user, **kwargs):
    session_cart_id = request.session.get('cart_id')
    print(f"Session cart ID: {session_cart_id}")
    if not session_cart_id:
        return

    session_cart_items = Cart.objects.filter(cart_id=session_cart_id, is_ordered=False)
    print(f"Session cart items: {session_cart_items}")
    
    if not session_cart_items.exists():
        return

    user_order, created = Order.objects.get_or_create(user=user, is_ordered=False)
    print(f"User order: {user_order}, created: {created}")

    for item in session_cart_items:
        user_cart_item, cart_created = Cart.objects.get_or_create(
            user=user,
            product=item.product,
            is_ordered=False
        )
        print(f"User cart item: {user_cart_item}, cart created: {cart_created}")

        if cart_created:
            user_cart_item.quantity = item.quantity
        else:
            user_cart_item.quantity += item.quantity
        
        user_cart_item.save()
        if user_cart_item not in user_order.product.all():
            user_order.product.add(user_cart_item)
    
    user_order.save()
    session_cart_items.delete()
    del request.session['cart_id']
    request.session.modified = True
