from django.contrib import admin

# Register your models here.
from .models import CustomUser,BlockedUser,Message,VibeMatch

admin.site.register(CustomUser)
admin.site.register(Message)
admin.site.register(VibeMatch)
admin.site.register(BlockedUser)
