from django.contrib import admin
from .models import Movie, Episode, Serie, Genre, Site, Season, Downloaded
from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number', 'acc_amount',)
    ordering = ['user','acc_amount',]
    search_fields = ('user',)

admin.site.register(Site)
admin.site.register(Movie)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Serie)
admin.site.register(Genre)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Downloaded)