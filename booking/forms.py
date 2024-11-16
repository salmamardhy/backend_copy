import random
import string
from django import forms
from django.shortcuts import get_object_or_404  
from account.models import Member
from booking.models import DraftBooking
from django.forms import ModelForm

class DraftBookingForm(ModelForm):
    WHATSAPP_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    # Use a ChoiceField for memberstatus
    whatsapp = forms.ChoiceField(
        choices=WHATSAPP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),  # Adding the class for styling
        label="Whatsapp Number"
    )

    # Tambahkan field memberstatus sebagai ModelChoiceField
    memberstatus = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        required=False,
        empty_label="Not a Member"
    )

    class Meta:
        model = DraftBooking
        fields = ['name', 'email', 'phone', 'event', 'referralid', 'bookingid', 'whatsapp', 'memberstatus']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}), 
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'event': forms.Select(),
            'referralid': forms.Select(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bookingid'].required = False
        self.fields['memberstatus'].required = False
        self.fields['referralid'].required = False
        # Pastikan field memberstatus menggunakan queryset yang benar
        self.fields['memberstatus'].queryset = Member.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generate bookingid if not provided
        if not instance.bookingid:
            event = self.cleaned_data.get('event')
            prefix = event.event_id if event else ''
            random_code = ''.join(random.choices(string.ascii_uppercase, k=5))
            instance.bookingid = prefix[:3] + random_code

        # Perbaikan logika untuk memberstatus
        email = self.cleaned_data.get('email')
        try:
            member = Member.objects.get(emailmain=email)
            instance.memberstatus = member
        except Member.DoesNotExist:
            instance.memberstatus = None

        # Pastikan referralid None jika tidak ada
        if not self.cleaned_data.get('referralid'):
            instance.referralid = None
            instance.referral_name = None

        if commit:
            instance.save()
        return instance
