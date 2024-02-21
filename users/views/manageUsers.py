from django.db.models import Avg, Sum
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from listings.models.listings import Listing
from listings.serializers import ListingSerializer
from users import models
from users.models import MyUser, Teacher
from users.serializers import ProfileSerializer, UpdateUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = request.user
            serializer = ProfileSerializer(data, context={'request': request})
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'გაუთვალისწინებელი ხარვეზი'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class check_user(APIView):
    def post(self, request):
        user = request.data.get('email')

        if not MyUser.objects.filter(email=user).exists():
            return Response(False)

        return Response(True)


class ManageUsers(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                try:
                    data = MyUser.objects.get(pk=pk)
                except:
                    return Response({'error': 'მომხმარებელი ვერ მოიძებნა'}, status.HTTP_404_NOT_FOUND)
                serializer = ProfileSerializer(data,context={'request': request})
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)

            paginator = PageNumberPagination()
            paginator.page_size = 12
            queryset = MyUser.objects.all().order_by('id')
            paginated_data = paginator.paginate_queryset(queryset, request)
            serializer = ProfileSerializer(paginated_data, many=True, context={'request': request})

            data = {
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'გაუთვალისწინებელი ხარვეზი'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopTenTeacher(APIView):
    def get(self, request):
        try:
            data = list(map(lambda x: x.user, Teacher.objects.all()))
            serializer = ProfileSerializer(data, many=True, context={'request': request})

            top_ten = sorted(serializer.data, key=lambda x: x['_score'], reverse=True)[:10]

            return Response({'data': top_ten}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'გაუთვალისწინებელი ხარვეზი'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataForSpecificTeacher(APIView):
    def post(self, request):
        try:
            listing_id = request.data['listing_id']
            listing = Listing.objects.get(id=listing_id)
            listing_serializer = ListingSerializer(listing, many=False, context={'request': request})
            _id = listing_serializer.data['teacher']
            user = MyUser.objects.get(is_teacher=True, id=_id)
            serializer = ProfileSerializer(user, many=False, context={'request': request})
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'error': "Listing not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UpdateProfileView(generics.UpdateAPIView):

    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer