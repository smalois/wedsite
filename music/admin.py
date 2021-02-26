from django.contrib import admin

from .models import SpotifyUser
from .models import Song
from .models import Device

admin.site.register(SpotifyUser)
admin.site.register(Song)
admin.site.register(Device)
