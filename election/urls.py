from django.contrib import admin
from django.urls import path,include

import vote

urlpatterns = [
    path('', include('vote.urls')),
    path('',include('voterecode.urls')),
    path('',include('authenticate.urls')),
    path('',include('ecbackend.urls')),
    path('admin/', admin.site.urls),
]
