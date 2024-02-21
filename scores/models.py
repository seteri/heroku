from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_delete, post_save

from listings.models.listings import Listing


class Score(models.Model):
    comment = models.CharField(max_length=255, null=True, blank=True, default=None)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    user = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)


    def update_scores(self):
        update_listing_score(self.listing)
        update_teacher_score(self.listing.teacher)


    def __str__(self):
        return f"{self.user} -> {self.listing} : {self.score}"


def update_scores(sender, instance, **kwargs):
    instance.update_scores()


post_save.connect(update_scores, sender=Score)
post_delete.connect(update_scores, sender=Score)


def update_listing_score(listing):
    avg_score = Score.objects.filter(listing=listing).aggregate(Avg('score'))['score__avg'] or 0
    listing._score = avg_score
    listing.save()


def update_teacher_score(teacher):
    listings = Listing.objects.filter(teacher=teacher)
    avg_score = listings.aggregate(Avg('_score'))['_score__avg'] or 0
    teacher._score = avg_score
    teacher.save()
