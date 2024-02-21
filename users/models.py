from uuid import uuid4
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from listings.models.listings import Listing


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_teacher, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_teacher=is_teacher
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_teacher=False

        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, )
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_email_confirmed = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Listing, related_name='favorited_by', blank=True)

    def add_to_favorites(self, listing):
        if not self.is_favorite(listing):
            self.favorites.add(listing)
            return True  # Indicate that the listing was added
        return False  # Indicate that the listing was already in favorites

    def remove_from_favorites(self, listing):
        if self.is_favorite(listing):
            self.favorites.remove(listing)
            return True  # Indicate that the listing was removed
        return False  # Indicate that the listing was not in favorites

    def is_favorite(self, listing):
        return self.favorites.filter(pk=listing.pk).exists()

    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{'teacher' if self.is_teacher else 'student'}: {self.first_name} {self.last_name} email: {self.email}"

    class Meta:
        verbose_name = "User",
        verbose_name_plural = 'Users'


class Teacher(models.Model):
    profile_pic = models.ImageField(upload_to='images/profile', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    cv = models.FileField(upload_to='files/', null=True, blank=True)
    phone = models.IntegerField(null=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)

    _score = models.DecimalField(default=0.0, decimal_places=2, max_digits=3)

    def __str__(self):
        return self.user.__str__()


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
