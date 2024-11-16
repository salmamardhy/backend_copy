# booking/cron.py
from datetime import timezone
from django.utils import timezone as django_timezone
from booking.models import DraftBooking

def update_booking_status():
    now = django_timezone.now()

    # Ambil semua booking yang statusnya aktif dan waktu expired_at-nya sudah lewat
    expired_bookings = DraftBooking.objects.filter(status='active', expires_at__lt=now)

    # Ubah status menjadi expired
    for booking in expired_bookings:
        booking.status = 'expired'
        booking.save()
