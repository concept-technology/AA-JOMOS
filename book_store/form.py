from django import forms
from django_countries.fields import CountryField
from  django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from book_store.widget import StarRatingWidget
from .models import *
from phonenumber_field.modelfields import PhoneNumberField

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=255, required=True, label="Newsletter Subject")
    heading = forms.CharField(max_length=255, required=True, label="Newsletter Heading")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Newsletter Content")
    url = forms.URLField(required=False, label="Call to Action URL (Optional)")


payment_choices= (
    ('paypal', 'paypal'),
    ('paystack', 'paystack'),

)

class UserProfileForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'country']

class CustomerRatingForm(forms.ModelForm):
    class Meta:
        model = CustomerRating
        fields = ['rating', 'headline', 'review']
        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '★☆☆☆☆'),
                    (2, '★★☆☆☆'),
                    (3, '★★★☆☆'),
                    (4, '★★★★☆'),
                    (5, '★★★★★')
                ],
                attrs={
                    'class': 'star-rating-select',  # Updated class for styling
                    'aria-label': 'Select rating',
                    'id': 'star-rating'
                }
            ),
            'headline': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Headline',
                    'aria-label': 'Headline'
                }
            ),
            'review': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write your review here...',
                    'rows': 4,
                    'aria-label': 'Review'
                }
            ),
        }
        labels = {
            'rating': 'Rating',
            'headline': 'Headline',
            'review': 'Review',
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
