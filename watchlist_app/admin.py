from django.contrib import admin

from watchlist_app.api.serializers import ReviewSerializer
from .models import WatchList, StreamPlatform, Review

admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)