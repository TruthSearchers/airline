from django.contrib import admin

from .models import Flights,Airport,Passenger

# Register your models here
class N(admin.ModelAdmin):
    list_display=("id","origin","destination","duration")

class P(admin.ModelAdmin):
    filter_horizontal=("flights",)

admin.site.register(Airport)
admin.site.register(Flights,N)
admin.site.register(Passenger,P)
