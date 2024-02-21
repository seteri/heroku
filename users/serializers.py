from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from django.contrib.auth import get_user_model
from users.models import Teacher, MyUser

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    profile_pic = serializers.ImageField(required=False)
    phone = serializers.IntegerField(required=False)
    bio = serializers.CharField(required=False, )
    cv = serializers.FileField(required=False)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                  'is_teacher',
                  'bio', 'cv', 'profile_pic', 'phone'
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        return get_profile(instance, context=self.context)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        email = data.get('email')
        errors = []
        if password != password2:
            errors.append('პაროლები არ ემთხვევა')
        if len(password) < 8:
            errors.append('პაროლი უნდა შედგებოდეს მინიმუმ 8 სიმბოლოსგან')
        if User.objects.filter(email=email).exists():
            errors.append('მომხმარებელი ამ იმეილით უკვე არსებობს')
        if len(errors) > 0:
            raise serializers.ValidationError({'errors': errors})
        return data

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            is_teacher=validated_data.get('is_teacher', False),
        )

        if user.is_teacher:
            Teacher.objects.create(
                user=user,
                bio=validated_data.get('bio'),
                cv=validated_data.get('cv'),
                profile_pic=validated_data.get('profile_pic'),
                phone=validated_data.get('phone')
            )
        return user


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        partial = True
        fields = ['id', 'email', 'first_name', 'last_name', 'is_teacher', 'is_email_confirmed']


class TeacherSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        partial = True
        fields = ['profile_pic', 'bio', 'cv', 'phone', '_score']

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return self.context.get('request').build_absolute_uri(obj.profile_pic.url)
        return None


class ProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False, )
    cv = serializers.FileField(required=False)
    phone = serializers.IntegerField()
    _score = serializers.DecimalField(read_only=True, max_digits=3, decimal_places=2)

    class Meta:
        model = MyUser
        partial = True
        fields = ['id', 'email', 'first_name', 'last_name',
                  'profile_pic', 'is_teacher',
                  'bio', 'cv', 'phone', '_score'
                  ]

        extra_kwargs = {
            'id': {'read_only': True},
        }

    def to_representation(self, instance):
        return get_profile(instance, context=self.context)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if instance["is_teacher"]:
            teacher = Teacher.objects.get(user=instance)
            t_serializer = TeacherSerializer()
            t_serializer.update(teacher, validated_data)
        return instance


def get_profile(instance: MyUser, context=None):
    representation = MyUserSerializer(instance).data
    if representation['is_teacher']:
        teacher_serializer = TeacherSerializer(Teacher.objects.get(user=instance), context=context)
        representation.update(teacher_serializer.data)
    return representation


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.save()

        return instance