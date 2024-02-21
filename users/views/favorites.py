from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from listings.models.listings import Listing
from listings.serializers import ListingSerializer
from users.serializers import MyUserSerializer


class AddToFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            listing_id = request.data['listing_id']
        except KeyError:
            return Response({"message": "განცხადების აიდი არაა მითითებული"}, status=status.HTTP_400_BAD_REQUEST)

        listing = get_object_or_404(Listing, pk=listing_id)

        if user.add_to_favorites(listing):
            serializer = MyUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "განცხადება უკვე ფავორიტებშია"}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            listing_id = request.data['listing_id']
        except KeyError:
            return Response({"message": "განცხადების აიდი არაა მითითებული"}, status=status.HTTP_400_BAD_REQUEST)

        listing = get_object_or_404(Listing, pk=listing_id)

        if user.remove_from_favorites(listing):
            serializer = MyUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "განცხადება არაა ფავორიტებში."}, status=status.HTTP_400_BAD_REQUEST)


class GetAllFavoritesOfUser(ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()