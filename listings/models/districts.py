from django.db import models

from listings.models.subjects import georgian_alphabet_validator


class District(models.Model):
    name = models.CharField(max_length=100, validators=[georgian_alphabet_validator])
    city = models.ForeignKey('listings.City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
