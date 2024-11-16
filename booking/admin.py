from django.contrib import admin
from .models import Event, DraftBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_time', 'cost')
    search_fields = ('event_id', 'event_name')

@admin.register(DraftBooking) 
class DraftBookingAdmin(admin.ModelAdmin):
    list_display = ('bookingid', 'name', 'event', 'referral_name', 'bookingstatus')
    search_fields = ('bookingid', 'name', 'email')
    readonly_fields = ('id','referral_name', 'created_at')
    list_filter = ('bookingstatus',)
    
    # Mengatur urutan fields di halaman detail
    fields = ('id', 'name', 'memberstatus', 'bookingid', 'email', 'phone', 'whatsapp', 
             'event', 'referralid', 'referral_name', 'bookingstatus', 
             'created_at', 'expires_at')

# from django.contrib import admin
# from django.db import models
# from account.models import Member  # Pastikan Anda mengimpor models dari django.db
# from .models import Event, DraftBooking

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('event_id', 'event_name', 'event_time', 'cost')
#     search_fields = ('event_id', 'event_name')

# @admin.register(DraftBooking) 
# class DraftBookingAdmin(admin.ModelAdmin):
#     list_display = ('bookingid', 'name', 'event', 'referral_name', 'bookingstatus', 'get_member_name', 'get_member_status_display')
#     search_fields = ('bookingid', 'name', 'email')
#     readonly_fields = ('id', 'referral_name', 'created_at')
#     list_filter = ('bookingstatus',)

#     # Menambahkan method untuk menampilkan status
#     def get_member_name(self, obj):
#         if obj.member_status == 'member':
#             # Misalnya, menggunakan referralid untuk mencari member terkait
#             member = Member.objects.filter(memberid=obj.referralid_id).first()
#             if member:
#                 return member.firstname + ' ' + member.lastname
#             return "Unknown Member"
#         return 'Not a Member'

#     get_member_name.short_description = 'Member Name'


#     # Mengatur urutan fields di halaman detail
#     fields = ('id', 'name', 'bookingid', 'email', 'phone', 'whatsapp', 
#              'event', 'referralid', 'referral_name', 'bookingstatus', 
#              'member_status', 'created_at', 'expires_at')

#     # Perbaikan pada formfield_overrides untuk menggunakan widget yang benar
#     formfield_overrides = {
#         models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'size': '20'})}
#     }