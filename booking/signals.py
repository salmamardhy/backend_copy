from datetime import timedelta
import os
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from .models import DraftBooking
from django.utils.html import strip_tags
from account.models import Users
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .models import DraftBooking

@receiver(post_save, sender=DraftBooking)
def create_payment_mail(sender, instance, created, **kwargs):
    if created:  # Only send the email if it's a new DraftBooking instance

        # Define the email subject and sender
        subject = "Alpha Seven Force Training Booking Confirmation"

        all_users = Users.objects.values_list('usermail', flat=True)
        receiver_email_sender = [instance.email]
        receiver_email_operator = all_users

        # Try to load the HTML email template
        try:
            # Create context with all required variables including logo
            context = {
                'name': instance.name,
                'event_name': instance.event.classname,
                'event_location': instance.event.vanue.vanuename + " - " + instance.event.vanue.location,
                'event_url': instance.event.vanue.vanuegmap,
                'event_time': instance.event.startdate.strftime("%B %d, %Y at %H:%M") + " WIB",
                'referral_name': instance.referralid.ktpname if instance.referralid else None,
                'payment_expired_wib': instance.payment_expires_at.strftime("%B %d, %Y at %H:%M") + " WIB",
                'payment_expired_sgt': (instance.payment_expires_at + timedelta(hours=1)).strftime("%B %d, %Y at %H:%M") + " SGT",
                'event_id': instance.event.classid,
                'phone': instance.phone,
                'email': instance.email,
            }

            # Render both HTML and plain text versions
            message_html_sender = render_to_string('payment_operator.html', context) #yg biasa
            message_html_operator = render_to_string('payment_operator2.html', context) #yg operator
            message_tele = render_to_string('payment_tele.html', context).strip()
            print('message_tele', message_tele)

            if message_html_sender:
                print("Template sender berhasil di-render")
            else:
                print("Template sender gagal di-render")

            if message_html_operator:
                print("Template operator berhasil di-render")
            else:
                print("Template operator gagal di-render")

            message_plain_sender = strip_tags(message_html_sender)
            message_plain_operator = strip_tags(message_html_operator)

            print("success")

        except Exception as e:
            # Fallback jika rendering template gagal
            print(f"Template rendering failed: {str(e)}")
            header = "Thank you for trusting A7F with your training needs. We have received the following booking:\n\n"
            body1 = f"Booker Name: {instance.name}\n" \
                    f"Event: {instance.event.classname}\n" \
                    f"Location: {instance.event.vanue.location}\n" \
                    f"Time: {instance.event.startdate}\n\n"
            body2 = "Payment can be made to the following accounts:\n" \
                    "a. BANK BCA Account Number: ....\n" \
                    "b. BANK BRI Account Number: ....\n\n"
            footer = "This offer is valid for 24 hours.\n\nBest regards,\nThe A7F Team"
            message_plain_operator = f"{header}{body1}{body2}{footer}"
            message_plain_sender = f"Operator Notification:\n\n{body1}{footer}"  # Default untuk operator
            message_html_sender = None
            message_html_operator = None  # Default untuk HTML operator

        # Send email to instance first
        send_mail(
            subject,
            message=message_plain_sender,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver_email_sender,
            fail_silently=False,
            html_message=message_html_sender
        )

        # Then send to all users
        send_mail(
            subject,
            message=message_plain_operator,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver_email_operator,
            fail_silently=False,
            html_message=message_html_operator
        )

                        # Send Telegram message using Selenium
        # try:
        #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #     driver.get("https://web.telegram.org/")
            
        #     # Wait for login
        #     input("Please log in to Telegram and press Enter...")

        #     # Search for the phone number in Telegram
        #     search_box = driver.find_element(By.CSS_SELECTOR, "input[data-peer-search='true']")
        #     search_box.send_keys(instance.phone)
        #     time.sleep(2)  # Wait for search results
        #     search_box.send_keys(Keys.ENTER)

        #     # Wait for chat to open and send the message
        #     time.sleep(2)
        #     message_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        #     message_box.send_keys(message_tele)
        #     message_box.send_keys(Keys.ENTER)

        #     print(f"Telegram message sent to {instance.phone} successfully.")
        #     driver.quit()

        # except Exception as e:
        #     print(f"Failed to send Telegram message: {str(e)}")
        #     if 'driver' in locals():
        #         driver.quit()

        # from django.shortcuts import render
        # from django.http import JsonResponse

        # import requests

        # def send_telegram_message(text, chat_id, token):
        #     url = f'https://api.telegram.org/bot{token}/sendMessage'
        #     payload = {'chat_id': chat_id, 'text': text}
        #     response = requests.post(url, data=payload)
        #     return response.json()

        # def send_telegram_photo(photo_url, chat_id, token):
        #     url = f'https://api.telegram.org/bot{token}/sendPhoto'
        #     payload = {'chat_id': chat_id, 'photo': photo_url}
        #     response = requests.post(url, data=payload)
        #     return response.json()

        # def send_message(request):
        #     if request.method == 'POST':
        #         chat_id = request.POST.get('chat_id')
        #         token = 'YOUR_BOT_TOKEN'  # Ganti dengan token bot Telegram kamu
        #         text = request.POST.get('message')
        #         photo_url = request.POST.get('photo_url')  # URL foto yang akan dikirim

        #         # Mengirim pesan
        #         send_telegram_message(text, chat_id, token)

        #         # Mengirim foto
        #         send_telegram_photo(photo_url, chat_id, token)

        #         return JsonResponse({'status': 'success', 'message': 'Pesan dan foto telah dikirim'})

        #     return render(request, 'payment_tele.html')



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
