from django.contrib import admin
from .models import Baby, Feeding, Changing, Doctor, Photo
import os

# Register your models here
admin.site.register(Baby)
admin.site.register(Feeding)
admin.site.register(Changing)
admin.site.register(Doctor)
admin.site.register(Photo)

def some_function(request):
    my_key = os.environ['SECRET_KEY']