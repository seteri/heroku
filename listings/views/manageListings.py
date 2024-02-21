from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from listings.models.listings import Listing
from listings.serializers import ListingSerializer, EditListingSerializer


class ManageListing(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_email_confirmed:
            return Response({
                'message': 'გაიარეთ იმეილის ვერიფიკაცია'
            }, status=status.HTTP_403_FORBIDDEN)
        if not user.is_teacher:
            return Response(
                {'error': 'იმისთვის რომ დადოთ განცხადება, უნდა იყოთ მასწავლებელი'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ListingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "თქვენი განცხადება წარმატებით გამოქვეყნდა", "message": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        try:
            user = request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'თქვენ არ შეგიძლიათ ამ განცხადების რედაქტირება'},
                    status=status.HTTP_403_FORBIDDEN
                )
            instance_id = self.request.query_params.get("id")

            if not Listing.objects.filter(teacher=user.id, id=instance_id).exists():
                return Response(
                    {'error': "ეს განცხადება არ არსებობს"},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing_instance = Listing.objects.get(id=instance_id, teacher=user.id)
            serializer = EditListingSerializer(listing_instance, data=request.data, partial=True,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'განცხადება წარმატებით განახლდა', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Listing.DoesNotExist:
            return Response(
                {'error': 'ასეთი ID-ით განცხადება არ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as a:
            print(a)
            return Response(
                {'error': 'შეცდომა განცხადების განახლებისას'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, format=None):
        try:
            user = request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'თქვენ არ შეგიძლიათ ამ განცხადების წაშლა'},
                    status=status.HTTP_403_FORBIDDEN
                )

            ID = self.request.query_params.get("id")

            if not Listing.objects.filter(teacher=user.id, id=ID).exists():
                return Response(
                    {'error': "ეს განცხადება არ არსებობს"},
                    status=status.HTTP_404_NOT_FOUND
                )
            Listing.objects.filter(teacher=user.id, id=ID).delete()

            if not Listing.objects.filter(teacher=user.id, id=ID).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': "განცხადება ვერ წაიშალა"},
                    status=status.HTTP_400_BAD_REQUEST
                )


        except:
            return Response(
                {'error': 'შეცდომა განცხადების წაშლისას'},

                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
