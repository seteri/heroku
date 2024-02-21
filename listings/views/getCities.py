from django.http import JsonResponse
from django.views import View

from listings.models.cities import City


class CityDistrictsView(View):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        data = []

        for city in cities:
            city_data = {
                'city_name': city.name,
                'districts': []
            }

            districts = city.district_set.all()
            for district in districts:
                city_data['districts'].append(district.name)

            data.append(city_data)

        return JsonResponse({'cities': data})
