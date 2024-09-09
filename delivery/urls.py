from django.urls import path
from . import views
app_name = 'delivery'
urlpatterns = [
    path('update-delivery-cost/', views.update_delivery_cost, name='update_delivery_cost'),
]
