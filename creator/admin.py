from django.contrib import admin
from creator.models import Creator, SocialLink
from catalog.models import YoutubeCatalog

admin.site.register(Creator)
admin.site.register(SocialLink)
admin.site.register(YoutubeCatalog)
