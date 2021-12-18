from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Region)
admin.site.register(Constituency)
admin.site.register(PollingStation)
admin.site.register(PoliticalParty)
admin.site.register(Tag)
