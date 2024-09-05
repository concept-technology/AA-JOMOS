from django.urls import path
from . import views
from .import cart_function

app_name ='store'

urlpatterns = [

     path('submit_rating/<str:slug>', views.product_detail, name='submit_rating'),
     
     
    path('category/', views.ProductCategories_view, name='categories-list'),
    path('category/<slug:slug>', views.product_list_by_category, name='product_list_by_category'),
#  
    path('', views.home_view,name='index'),
      
    path('signup/',views.register, name='signup'),
    
    path('login', views.login, name='login'),
    path('update-cart-size/', views.update_cart_color_and_qty, name='update_cart_size'),
    
# cart section
     path('cart-count/', views.cart_count_view, name='cart-count'),    
    #  path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    #  path('add-to-cart/',views.AddToCartView.as_view(), name='add-to-cart'),
     path('delete-from-cart/',views.delete_cart, name='delete-from-cart'),
     path('update-cart/', views.UpdateCartQuantity.as_view(), name='update_cart_quantity'),
     path('cart/', views.CartView.as_view(), name='cart'),
    #  path('cart/<slug>', views.CartView.as_view(), name='cart_item'),
     path('delete-cart-item/', views.delete_cart, name='delete-cart-item'),
     
    # checkout' s
     path('cart/proceed-to-checkout',views.CheckoutView.as_view(), name='check-out'),
     
     
     
     path('account/profile/dash-board', views.DashBoardView.as_view(), name='dash-board' ),
     
   
     path('order/payment/', views.initiate_payment, name='initiate_payment'),
     
     path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
     
     path('refund-request', views.RequestRefund.as_view(), name='refund-request'),
     
     path('verify-address', views.verify_address_and_pay, name='verify-address'),

     
     path('address/edit/<int:pk>', views.Update_addressView, name='update-address'),
     
     
     path('apply-coupon/', views.apply_coupon, name='apply-coupon'),
     

     path('search/', views.search_view, name='search'),
     
     path('product/<slug>', views.product_detail, name='product-detail'),
     
     
     path('order/<int:order_id>/received/', views.mark_order_as_received, name='mark-order-received'),
     
    
    path('view/next_product/<slug>', views.next_product, name='next_product'),
    
    path('contact/', views.contact_view, name='contact'),
    
    path('payment/success', views.success_page, name='success-page'),
    path('add-to-wishlist/<int:product_id>/', views.toggle_wishlist, name='add-to-wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('wishlist-count/', views.wishlist_count, name='wishlist-count'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    path('rate/product/<str:slug>', views.rate_product, name='rate_product'),   
  path('accounts/confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view(), name='account_confirm_email'),
   path('load-cities/', views.load_cities, name='load_cities')
  # Other URL patterns...
]




