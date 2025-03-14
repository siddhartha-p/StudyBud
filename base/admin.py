from django.contrib import admin #type:ignore
from .models import Room,Message,Topic

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)