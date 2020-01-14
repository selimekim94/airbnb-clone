from django.db import models
from core.models import TimeStampedModel
from users.models import User
from rooms.models import Room


class Review(TimeStampedModel):
    """ Review Model Definition """
    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review[:50]} - {self.room}'
