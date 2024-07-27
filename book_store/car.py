@csrf_exempt
@require_POST
def add_to_cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        slug = request.POST.get('slug')
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get('quantity', 1))  # Default quantity to 1 if not provided

        if request.user.is_authenticated:
            cart_qs = Cart.objects.filter(user=request.user, product=product, is_ordered=False)

            if cart_qs.exists():
                cart_item = cart_qs.first()
                cart_item.quantity += quantity  # Increment the quantity
                cart_item.save()
                messages.success(request, f"Updated {product.title} quantity in cart")
            else:
                cart_item = Cart.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
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

            storage = get_messages(request)
            response_messages = [{'message': message.message, 'tags': message.tags} for message in storage]

            return JsonResponse({'success': True, 'cart_count': Cart.objects.filter(user=request.user, is_ordered=False).count(), 'messages': response_messages})
        else:
            # Handle cart for anonymous users
            cart = request.session.get('cart', {})

            if str(product.id) in cart:
                cart[str(product.id)]['quantity'] += quantity
                messages.success(request, f"Updated {product.title} quantity in cart")
            else:
                cart[str(product.id)] = {
                    'product_id': product.id,
                    'title': product.title,
                    'quantity': quantity
                }
                messages.success(request, f"{product.title} is added to cart")

            request.session['cart'] = cart
            request.session.modified = True  # Ensure session is saved

            storage = get_messages(request)
            response_messages = [{'message': message.message, 'tags': message.tags} for message in storage]

            return JsonResponse({'success': True, 'cart': request.session.get('cart', {}), 'messages': response_messages})

    return JsonResponse({'message': 'error processing your request'}, status=400)
