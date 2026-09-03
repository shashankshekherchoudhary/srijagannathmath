from django import forms
from .models import ContactMessage


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
            }),
        }

    def clean_website(self):
        """Honeypot check: if this hidden field is filled, it's a bot."""
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Bot detected.')
        return ''

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            # Remove spaces and dashes for validation
            cleaned = phone.replace(' ', '').replace('-', '').replace('+', '')
            if not cleaned.isdigit() or len(cleaned) < 10:
                raise forms.ValidationError('Please enter a valid phone number.')
        return phone
