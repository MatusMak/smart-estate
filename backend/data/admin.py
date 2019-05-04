from django.contrib import admin

from .models import *

admin.site.register(Parking)
admin.site.register(Timeslot)
admin.site.register(Usage)
admin.site.register(AirStation)
