from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import (
    WatchListSerializer, 
    StreamPlatformSerializer,
    ReviewSerializer
)

from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import (
    IsAdminOrReadOnly, 
    IsReviewUserOrReadOnly
)


class ReviewCreate(generics.CreateAPIView):
    """Creates a list of reviews for a given movie"""
    queryset = Review.objects.all()
    serializer_class  = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Create a review for a given movie,
        User are only allowed to post one review per movie
        """
        # Get Primary Key
        pk = self.kwargs["pk"] 

        # Get specific movie
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user

        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist!!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (serializer.validated_data["rating"] + watchlist.avg_rating) / 2

        watchlist.number_rating += 1
        watchlist.save()

        # Save For particular movie as the foreign key
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    """Display a list of reviews for a particular movie"""
    # permission_classes = [IsAuthenticated]
    # queryset = Review.objects.all()
    serializer_class  = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Created Review Updating, retrieving and deleting for owner"""
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class  = ReviewSerializer

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) # create response
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"Error", "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"Error", "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # create response
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"Error", "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
            
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()

        serializer = StreamPlatformSerializer(platforms, many=True, context={"request": request})

        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform, context={"request": request})

            return Response(serializer.data)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Platform not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(platform, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Streaming platform not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "Streaming platform not found"},
                status=status.HTTP_404_NOT_FOUND
            )

# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]















# class ReviewList(
#         mixins.ListModelMixin,
#         mixins.CreateModelMixin,
#         generics.GenericAPIView
#     ):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(
#         mixins.RetrieveModelMixin,
#         generics.GenericAPIView
#     ):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)














# @api_view(["GET", "POST"])
# def movie_list(request):
#     if request.method == "GET":
#         movies = WatchList.objects.all() # Get all movies
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = WatchListSerializer(data=request.data)
        
#         # Check validity
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201) # create response
#         else: 
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET", "PUT", "DELETE"])
# def movie_detail(request, pk):
    
#     if request.method == "GET":
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"Error", "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
            
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == "PUT":
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"Error", "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(movie, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data) # create response
#         else: 
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == "DELETE":
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"Error", "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
            
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        