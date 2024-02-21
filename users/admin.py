from django.contrib import admin

from .forms import MyUserCreationForm
from users.models import MyUser, Teacher


class MyUserAdmin(admin.ModelAdmin):
    model = MyUser
    add_form = MyUserCreationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('email', "password1", "password2", 'first_name',
                           'last_name', 'is_active', 'is_teacher'),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class TeacherAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.user.email

    list_display = ['email', '_score']


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
