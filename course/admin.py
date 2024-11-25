from django.contrib import admin
from django.apps import apps

# Ganti 'newapp' dengan nama aplikasi Anda
app = apps.get_app_config('course')

# Daftarkan setiap model ke admin
for model in app.get_models():
    admin.site.register(model)