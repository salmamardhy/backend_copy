# import os
# from django.db.models.signals import post_save
# from django.conf import settings
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.templatetags.static import static
# from .models import DraftBooking, Event
# from django.utils.html import strip_tags
# # import time
# # import webbrowser as web
# # import pyautogui as pg

# @receiver(post_save, sender=DraftBooking)
# def create_payment_mail(sender, instance, created, **kwargs):
#     if created:  # Only send the email if it's a new DraftBooking instance
        
#         # Define the email subject and sender
#         subject = "Alpha Seven Force Training Booking Confirmation"
#         receiver_email = [instance.email]
        
#         # Try to load the HTML email template
#         try:
#             # Create context with all required variables including logo
#             context = {
#                 'name': instance.name,
#                 'event_name': instance.event.event_name,
#                 'event_url': instance.event.event_url,
#                 'event_time': instance.event.event_time,
#                 'referral_name': instance.referralid.ktpname,
#                 'payment_expires_at': instance.payment_expires_at,
#                 'event_id': instance.event.event_id,
#             }

#             # Render both HTML and plain text versions
#             message_html = render_to_string('payment_instructions.html', context)
#             message_plain = strip_tags(message_html)

#             print("success")

#         except Exception as e:
#             # Fallback if template rendering fails
#             print(f"Template rendering failed: {str(e)}")
#             header = "Thank you for trusting A7F with your training needs. We have received the following booking:\n\n"
#             body1 = f"Booker Name: {instance.name}\n" \
#                     f"Event: {instance.event.event_name}\n" \
#                     f"Location: {instance.event.event_url}\n" \
#                     f"Time: {instance.event.event_time}\n\n"
#             body2 = "Payment can be made to the following accounts:\n" \
#                     "a. BANK BCA Account Number: ....\n" \
#                     "b. BANK BRI Account Number: ....\n\n"
#             footer = "This offer is valid for 24 hours.\n\nBest regards,\nThe A7F Team"
#             message_plain = f"{header}{body1}{body2}{footer}"
#             message_html = None

#         # Send the email
#         send_mail(
#             subject,
#             message=message_plain,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=receiver_email,
#             fail_silently=False,
#             html_message=message_html
#         )

#         # if instance.whatsapp_number:
#         #     try:
#         #         # Format nomor WhatsApp harus dengan kode negara, misalnya +628xxxxxxxxx
#         #         whatsapp_url = f"https://web.whatsapp.com/send?phone={instance.whatsapp_number}&text=" \
#         #                        f"Booking Confirmation\n\n" \
#         #                        f"Name: {instance.name}\n" \
#         #                        f"Event: {instance.event.event_name}\n" \
#         #                        f"Event URL: {instance.event.event_url}\n" \
#         #                        f"Time: {instance.event.event_time}\n\n" \
#         #                        "Please make a payment to the following accounts:\n" \
#         #                        "BANK BCA: ....\n" \
#         #                        "BANK BRI: ....\n\n" \
#         #                        "This offer is valid for 24 hours.\n\n" \
#         #                        "Best regards,\nThe A7F Team"

#         #         # Membuka WhatsApp Web dengan URL
#         #         web.open(whatsapp_url)

#         #         # Tunggu beberapa detik hingga WhatsApp Web terbuka
#         #         time.sleep(10)

#         #         # Tekan Enter untuk mengirim pesan
#         #         pg.press('enter')
#         #     except Exception as e:
#         #         print(f"Failed to send WhatsApp message: {str(e)}")
