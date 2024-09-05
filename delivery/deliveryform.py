from.models import DeliveryLocations
from django import forms
from book_store.models import CustomersAddress

class LocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocations
        fields = ['state']
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        locations = DeliveryLocations.objects.all()
        location_choices = [(location.id, location.state) for location in locations]
        self.fields['state'].widget = forms.Select(choices=location_choices, attrs={'class': 'form-control'})



class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomersAddress
        fields = ['street_address', 'apartment', 'town', 'state', 'telephone', 'zip_code', 'country', 'message']
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby landmark'}),
             'town': forms.Select(attrs={'class': 'form-control', 'id': 'id_town'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'state': forms.Select(attrs={'class': 'form-control', 'id': 'state-select'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08099999999'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Do you have any message about your delivery? (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        # Get distinct states
        abuja_states = DeliveryLocations.objects.values('state').distinct()
        self.fields['state'].choices = [(state['state'], state['state']) for state in abuja_states]
        self.fields['town'].choices = []  # Initially empty until state is selected
        # self.fields['town'].widget.attrs.update({'id': 'id_town'})
