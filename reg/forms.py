from django import forms
from django.core.validators import ip_address_validators, validate_ipv4_address
from django.core.exceptions import ValidationError

class ScanForm(forms.Form):

    target = forms.GenericIPAddressField(label='Target IP', required=True)

    def clean(self):
        cleaned_data = super(ScanForm, self).clean()
        target = self.cleaned_data.get('target')
        print("in cleaner, target is {0}".format(target))
        try:
            validate_ipv4_address(target)
        except ValidationError:
            raise forms.ValidationError(
                "Invalid IP address")

        print("cleaned data : {0}".format(cleaned_data))

        return cleaned_data