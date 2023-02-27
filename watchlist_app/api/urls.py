from django.urls import path, include
from watchlist_app.api.serializers import ReviewSerializer
# from . import views
from watchlist_app.api.views import (
    WatchListAV, 
    WatchDetailAV,
    StreamPlatformAV, 
    StreamPlatformDetailAV,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformVS
)
from rest_framework.routers import DefaultRouter

# Router Creation
router = DefaultRouter()
# router.register('stream', StreamPlatformVS, basename='streamplatform')
router.register(r'stream', StreamPlatformVS)


urlpatterns = [
    path("list/", WatchListAV.as_view(), name="watch-list"),
    path("<int:pk>/", WatchDetailAV.as_view(), name="watch-detail"),


    # path('', include(router.urls)),
    path("stream/", StreamPlatformAV.as_view(), name="stream-list"),
    path("stream/<int:pk>/", StreamPlatformDetailAV.as_view(), name="stream-detail"),

    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review-create"),
    path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"), # Delete, Create, Post

    # path("review/", ReviewList.as_view(), name="review-list"),
    # path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
]