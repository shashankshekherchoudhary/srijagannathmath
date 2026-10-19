import re
import logging
from django import forms
from .models import ContactMessage

logger = logging.getLogger('core')


class ContactForm(forms.ModelForm):
    # Honeypot anti-spam field: hidden from users, bots auto-fill it
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
        label='',
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (optional)',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True,
                'maxlength': '5000',
            }),
        }

    def clean_website(self):
        """Honeypot check: if this hidden field is filled, it's a bot."""
        if self.cleaned_data.get('website'):
            logger.warning("Spam bot detected and blocked via honeypot 'website' field.")
            raise forms.ValidationError('Bot detected.')
        return ''

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            # Enforce max storage length first to protect database column
            if len(phone) > 20:
                raise forms.ValidationError('Phone number must not exceed 20 characters.')
            # Extract digits only to validate numerical integrity and international length
            digits = re.sub(r'\D', '', phone)
            if len(digits) < 10 or len(digits) > 15:
                raise forms.ValidationError('Please enter a valid phone number (10 to 15 digits).')
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) > 5000:
            raise forms.ValidationError('Message must not exceed 5000 characters.')
        return message
