from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from listings.models.cities import City
from listings.serializers import CitySerializer, DistrictSerializer


class CityListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            if not City.objects.exists():
                return Response(
                    {'error': 'ქალაქები ვერ მოიძებნა'},
                    status=status.HTTP_404_NOT_FOUND
                )
            cities = City.objects.all()
            cities_serializer = CitySerializer(cities, many=True)
            return Response({
                'data': cities_serializer.data
            }, status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'შეცდომა ინფორმაციის მიღებისას'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, city_id):
        try:
            try:
                city = City.objects.get(pk=city_id)
            except City.DoesNotExist:
                return Response({'error': 'ქალაქი ვერ მოიძებნა'}, status=404)

            city_serializer = CitySerializer(city)
            districts = city.district_set.all()

            response_data = {
                'city': city_serializer.data,
            }

            if districts.exists():
                district_serializer = DistrictSerializer(districts, many=True)
                response_data['districts'] = district_serializer.data

            return Response(response_data)

        except:
            return Response(
                {'error': 'შეცდომა ინფორმაციის მიღებისას'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
