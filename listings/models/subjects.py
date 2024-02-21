from django.core.validators import RegexValidator
from django.db import models

georgian_alphabet_validator = RegexValidator(
    regex=r'^[ა-ჰ\s]+$',
    message='მიუთითეთ მხოლოდ ქართული ასოები',
    code='invalid_georgian_alphabet'
)

class Subject(models.Model):
    name = models.CharField(max_length=100, validators=[georgian_alphabet_validator])

    def __str__(self):
        return self.name
