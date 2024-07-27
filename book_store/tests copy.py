from django.test import TestCase

# Create your tests here.

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    response = HttpResponse()

    if request.user.is_authenticated:
        cart_qs = Cart.objects.filter(user=request.user, product=product, is_ordered=False)

        if cart_qs.exists():
            cart_item = cart_qs.first()
            cart_item.is_in_cart = True
            cart_item.quantity += 1  # Increment the quantity
            cart_item.save()
            messages.success(request, f"Updated {product.title} quantity in cart")
        else:
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=1,
                is_ordered=False
            )
            messages.success(request, f"{product.title} is added to cart")

        # Create or update the order
        order_qs = Order.objects.filter(user=request.user, is_ordered=False)
        if order_qs.exists():
            order = order_qs.first()
        else:
            order = Order.objects.create(
                user=request.user,
                reference=f'order-{secrets.token_hex(8)}',
                date=timezone.now(),
                is_ordered=False
            )

        order.product.add(cart_item)
        order.save()

    else:
        # Handle cart for anonymous users using a unique identifier
        cart_id = request.COOKIES.get('cart_id')

        if not cart_id:
            cart_id = str(uuid.uuid4())
            response.set_cookie('cart_id', cart_id)
            
        cart_qs = Cart.objects.filter(product=product, is_ordered=False)

        if cart_qs.exists():
            cart_item = cart_qs.first()
             # Increment the quantity
            cart_item.save()
            messages.error(request, f" {product.title} is already in cart")
        else:
            cart_item = Cart.objects.create(
                cart_id=cart_id,
                product=product,
                quantity=1,
                is_ordered=False
            )
            messages.success(request, f"{product.title} is added to cart")

        # Create or update the order for the anonymous user
        order_qs = Order.objects.filter(cart_id=cart_id, is_ordered=False)
        if order_qs.exists():
            order = order_qs.first()
        else:
            order = Order.objects.create(
                cart_id=cart_id,
                reference=f'order-{secrets.token_hex(8)}',
                date=timezone.now(),
                is_ordered=False
            )

        order.product.add(cart_item)
        order.save()
        
        print(order.product)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    return redirect("store:index")
