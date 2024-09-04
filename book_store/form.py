from django import forms
from django_countries.fields import CountryField
from  django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from book_store.widget import StarRatingWidget
from .models import *


class AbujaLocationForm(forms.ModelForm):
    class Meta:
        model = AbujaLocation
        fields = ['pick_up_location']

    def __init__(self, *args, **kwargs):
        super(AbujaLocationForm, self).__init__(*args, **kwargs)
        locations = AbujaLocation.objects.all()
        location_choices = [(location.id, location.state) for location in locations]
        self.fields['pick_up_location'].widget = forms.Select(choices=location_choices, attrs={'class': 'form-control'})
       
payment_choices= (
    ('paypal', 'paypal'),
    ('paystack', 'paystack'),

)

class UserProfileForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



class CustomerRatingForm(forms.ModelForm):
    class Meta:
        model = CustomerRating
        fields = ['rating','headline', 'review']
        widgets = {
            'rating': forms.Select(choices=[
                (1, '★☆☆☆☆'),
                (2, '★★☆☆☆'),
                (3, '★★★☆☆'),
                (4, '★★★★☆'),
                (5, '★★★★★')
            ], attrs=({
                'class': 'form-control star',
                'id':'star'
            }))
        }

class CouponForm(forms.Form):
       code =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'placeholder': 'Have a coupon? Click here to enter your code'
        }
    )),max_length=10)


class RefundRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'email' 
        }
        )))
    reference_code =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'order reference'
        }
        )),max_length=15)
    message =forms.CharField(widget=forms.Textarea(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'reason for refund'
        }
    )),max_length=1000)
    


state_choices= (
    ('Abia', 'Abia'),
    ('Adamawa','Adamawa'),
    ('Akwa Ibom','Akwa Ibom'),
    ('Anambra','Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River','Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu','Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau','Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('FCT', 'Federal Capital Territory (FCT)')
)
     

class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomersAddress
        fields = ['street_address', 'apartment', 'town', 'state', 'telephone', 'zip_code', 'country', 'message']   
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby landmark'}),
            'town': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Town'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08099999999'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Do you have any message about your delivery? (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['state'].choices = [(state['state'], state['state']) for state in AbujaLocation.objects.values('state').distinct()]
       
class CartUpdateForm(forms.Form):
    pk  = forms.IntegerField()
    size = forms.CharField(max_length=15)
    quantity = forms.IntegerField()
         
# class CheckoutForm(forms.Form):
#     street_address = forms.CharField(widget=forms.TextInput(attrs=(
#         {
#             'placeholder':'street name',
#             'class': 'form-control',
#             'required': True
#         }
#     )))
#     apartment = forms.CharField(widget=forms.TextInput(attrs=(
#         {
#             'placeholder':'apartments, suite, unit etc ...',
#             'class': 'form-control',
#             'required': True
#         }
#     )))
#     town =forms.CharField(widget=forms.TextInput(attrs=(
#         {
#             'class': 'form-control',
#             'required': True
#         }
#     )))
#     state = forms.CharField(widget=forms.TextInput(attrs=(
#         {
#             'class': 'form-control',
#             'required': True
#         }
#     )))
#     # telephone = forms.NumberInput(widget=forms.NumberInput(attrs=(
#     #     {
#     #         'class': 'form-control',
#     #         'required': True
#     #     }
#     # )))
#     country = CountryField(blank_label="select_country").formfield(widget=CountrySelectWidget(attrs=(
#         {
#             'class': 'from-control'
#         }
#     )))
       
#     zip_code =forms.CharField(widget=forms.TextInput(attrs=(
#         {
#             'class': 'form-control',
#             'required': True
#         }
#     )),max_length=10)
#     payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=payment_choices)
