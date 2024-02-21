from django.db import models

from listings.models.subjects import georgian_alphabet_validator


class City(models.Model):
    name = models.CharField(max_length=100,  validators=[georgian_alphabet_validator])

    def __str__(self):
        return self.name
