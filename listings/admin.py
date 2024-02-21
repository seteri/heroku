from django.contrib import admin

from listings.models.cities import City
from listings.models.currency import Currency
from listings.models.districts import District
from listings.models.listings import Listing
from listings.models.subjects import Subject


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ListingAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'title','_score']


admin.site.register(Currency)

admin.site.register(Subject)
admin.site.register(Listing, ListingAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
