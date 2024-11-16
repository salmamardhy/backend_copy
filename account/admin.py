# from django.contrib import admin
# from .models import Member

# class MemberAdmin(admin.ModelAdmin):
#     list_display='memberid', 'ktpname', 'namatengah'

# admin.site.register(Member,MemberAdmin)

from django.contrib import admin
from django.apps import apps

# Ganti 'newapp' dengan nama aplikasi Anda
app = apps.get_app_config('account')

# Daftarkan setiap model ke admin
for model in app.get_models():
    admin.site.register(model)

# from django.contrib import admin
# from django.apps import apps

# # Ganti 'newapp' dengan nama aplikasi Anda
# app = apps.get_app_config('newapp')

# # Contoh kustomisasi untuk model tertentu
# class MemberAdmin(admin.ModelAdmin):
#     list_display = ('field1', 'field2')  # Ganti dengan nama field yang sesuai

# admin.site.register(Member, MemberAdmin)

# # Daftarkan model lainnya secara dinamis
# for model in app.get_models():
#     if model.__name__ != 'Member':  # Menghindari pendaftaran model yang sama
#         admin.site.register(model)