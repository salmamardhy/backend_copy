import os
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import DraftBooking, Event
from django.utils.html import strip_tags
import time
import webbrowser as web
import pyautogui as pg

@receiver(post_save, sender=DraftBooking)
def create_payment_mail(sender, instance, created, **kwargs):
    if created:  # Only send the email if it's a new DraftBooking instance
        
        # Define the email subject and sender
        subject = "Booking Confirmation and Payment Instructions"
        receiver_email = [instance.email]
        
        # Try to load the HTML email template
        try:
            # Use Django's render_to_string to render the HTML template
            email_content = render_to_string('payment_instructions.html', {
                'name': instance.name,
                'event_name': instance.event.event_name,
                'event_url': instance.event.event_url,
                'event_time': instance.event.event_time,
            })
            print("success")

        except FileNotFoundError:
            # Fallback if the template is not found
            # Fallback to plain text message
            header = "Thank you for trusting A7F with your training needs. We have received the following booking:\n\n"
            body1 = f"Booker Name: {instance.name}\n" \
                    f"Event: {instance.event.event_name}\n" \
                    f"Location: {instance.event.event_url}\n" \
                    f"Time: {instance.event.event_time}\n\n"
            body2 = "Payment can be made to the following accounts:\n" \
                    "a. BANK BCA Account Number: ....\n" \
                    "b. BANK BRI Account Number: ....\n\n"
            footer = "This offer is valid for 24 hours.\n\nBest regards,\nThe A7F Team"
            email_content = f"{header}{body1}{body2}{footer}"

        # Send the email with both plain text and HTML
        plain_message = strip_tags(email_content)

        send_mail(
            subject,
            message=plain_message,  # Leave plain text message empty if you're using HTML
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver_email,
            fail_silently=False,
            html_message=email_content  # Pass the rendered HTML as html_message
        )

        # if instance.whatsapp_number:
        #     try:
        #         # Format nomor WhatsApp harus dengan kode negara, misalnya +628xxxxxxxxx
        #         whatsapp_url = f"https://web.whatsapp.com/send?phone={instance.whatsapp_number}&text=" \
        #                        f"Booking Confirmation\n\n" \
        #                        f"Name: {instance.name}\n" \
        #                        f"Event: {instance.event.event_name}\n" \
        #                        f"Event URL: {instance.event.event_url}\n" \
        #                        f"Time: {instance.event.event_time}\n\n" \
        #                        "Please make a payment to the following accounts:\n" \
        #                        "BANK BCA: ....\n" \
        #                        "BANK BRI: ....\n\n" \
        #                        "This offer is valid for 24 hours.\n\n" \
        #                        "Best regards,\nThe A7F Team"

        #         # Membuka WhatsApp Web dengan URL
        #         web.open(whatsapp_url)

        #         # Tunggu beberapa detik hingga WhatsApp Web terbuka
        #         time.sleep(10)

        #         # Tekan Enter untuk mengirim pesan
        #         pg.press('enter')
        #     except Exception as e:
        #         print(f"Failed to send WhatsApp message: {str(e)}")
