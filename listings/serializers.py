from rest_framework import serializers

from listings.models.cities import City
from listings.models.districts import District
from listings.models.listings import Listing
from listings.models.subjects import Subject
from users.serializers import ProfileSerializer


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = District
        fields = ('id', 'name', 'city')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('city', None)
        return representation


class ListingSerializer(serializers.ModelSerializer):
    _photo = serializers.SerializerMethodField()
    _city = serializers.SerializerMethodField()
    _district = serializers.SerializerMethodField()
    _subject = serializers.SerializerMethodField()
    _teacher = serializers.SerializerMethodField()
    _phone = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = (
            'id', 'title', 'teacher', 'description', 'price',
            'city', 'district', 'subject', 'photo',
            '_city', '_district', '_subject', '_photo',
            'date_created', 'views', '_teacher', '_phone'
        )

        extra_kwargs = {
            'city': {'write_only': True},
            'district': {'write_only': True},
            'subject': {'write_only': True},
            'photo': {'write_only': True}
        }

    def get__photo(self, obj):
        if obj.photo:
            return self.context.get('request').build_absolute_uri(obj.photo.url)
        return None

    def get__city(self, obj):
        if obj.city:
            return obj.city.name

    def get__teacher(self, obj):
        if obj.city:
            return obj.teacher.user.first_name

    def get__phone(self, obj):
        if obj.city:
            return obj.teacher.phone

    def get__district(self, obj):
        if obj.district:
            return obj.district.name

    def get__subject(self, obj):
        if obj.subject:
            return obj.subject.name

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'city' in representation and representation['city'] is None:
            representation.pop('city')
        if 'district' in representation and representation['district'] is None:
            representation.pop('district')
        return representation

    def validate(self, data):
        price = data.get('price')
        errors = []
        district = data.get('district')
        city = data.get('city')
        if district is not None and city is not None and district.city != city:
            raise serializers.ValidationError({'error': 'District does not belong to the specified city'})
        if price < 0:
            errors.append('ფასი უნდა იყოს დადებითი რიცხვი')
        if len(errors) > 0:
            raise serializers.ValidationError({'errors': errors})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'teacher'):
            teacher = user.teacher
            validated_data['teacher'] = teacher
            listing = Listing.objects.create(**validated_data)
            return listing
        else:
            raise serializers.ValidationError({'error': 'User does not have a teacher attribute'})


class ListingWithTeacherSerializer(ListingSerializer):
    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + ('teacher',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        teacher_instance = instance.teacher
        if teacher_instance:
            user_instance = teacher_instance.user
            profile_serializer = ProfileSerializer(user_instance, context=self.context)
            representation['teacher'] = {
                'name': profile_serializer.data['first_name'],
                'phone': profile_serializer.data['phone'],
                'profile_pic': profile_serializer.data['profile_pic']
            }
        else:
            representation['teacher'] = None
        return representation


class EditListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'price', 'city', 'district', 'subject', 'photo')
        partial = True

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'city' in representation and representation['city'] is None:
            representation.pop('city')
        if 'district' in representation and representation['district'] is None:
            representation.pop('district')
        return representation

    def validate(self, data):
        price = data.get('price')
        errors = []
        district = data.get('district')
        city = data.get('city')
        if district is not None and city is not None and district.city != city:
            raise serializers.ValidationError({'error': 'ეს უბანი მითითებულ ქალაქს არ ეკუთვნის'})

        if price and price < 0:
            errors.append('ფასი უნდა იყოს დადებითი რიცხვი')

        if len(errors) > 0:
            raise serializers.ValidationError({'errors': errors})

        return data


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

