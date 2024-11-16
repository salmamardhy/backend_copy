from datetime import timedelta, datetime
from django.utils import timezone
from django.db import models
import string
import random
from account.models import Member
import pytz

class Event(models.Model):
    event_id = models.CharField(primary_key=True, max_length=10)
    event_name = models.CharField(max_length=100)
    event_url = models.URLField(null=True, blank=True)
    event_photo = models.URLField(null=True, blank=True)
    event_time = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if "drive.google.com" in self.event_photo:
            self.event_photo = self.event_photo.replace("/view?usp=sharing", "")
            self.event_photo = self.event_photo.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.event_name
    
    class Meta:
        db_table = 'event'

class DraftBooking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bookingid = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    whatsapp = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    referralid = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    referral_name = models.CharField(max_length=100, null=True, blank=True, editable=False)

    BOOKINGSTATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    bookingstatus = models.CharField(max_length=10, choices=BOOKINGSTATUS_CHOICES, default='active')
    # Perbaikan pada field memberstatus agar terhubung ke tabel Member
    memberstatus = models.ForeignKey(
        Member, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='member_bookings'  # Mengubah related_name agar lebih jelas
    )

    PAYMENTSTATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'), # menunggu pembayaran
        ('cancelled', 'Cancelled'),
        ('onhold', 'On Hold'), # menunggu verifikasi pembayaran
    ]
    paymentstatus = models.CharField(max_length=10, choices=PAYMENTSTATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    payment_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('bookingid', 'id')
        db_table = 'draftbooking'
        verbose_name = 'Draft Booking'
        verbose_name_plural = 'Draft Bookings'

    def __str__(self):
        return f"Booking ID: {self.bookingid}"

    def save(self, *args, **kwargs):
        if not self.id:
            last_booking = DraftBooking.objects.order_by('-id').first()
            self.id = (last_booking.id + 1) if last_booking else 1

        if not self.created_at:
            self.created_at = timezone.now()

        if not self.expires_at:
            # Ensure created_at is a datetime object before adding timedelta
            if isinstance(self.created_at, str):
                self.created_at = timezone.make_aware(datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S"))
            self.expires_at = self.created_at + timedelta(minutes=10)

        if not self.payment_expires_at:
            if isinstance(self.created_at, str):
                self.created_at = timezone.make_aware(datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S"))
            self.payment_expires_at = self.created_at + timedelta(minutes=10)

        # Jika referralid tidak ada, pastikan referral_name juga None
        if not self.referralid:
            self.referralid = None
            self.referral_name = None
        else:
            self.referral_name = self.referralid.ktpname

        # Ensure expires_at is a datetime object for comparison
        if isinstance(self.expires_at, str):
            self.expires_at = timezone.make_aware(datetime.strptime(self.expires_at, "%Y-%m-%d %H:%M:%S"))
            
        if timezone.now() > self.expires_at:
            self.bookingstatus = 'expired'

        super(DraftBooking, self).save(*args, **kwargs)