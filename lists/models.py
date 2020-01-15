from django.db import models
from core.models import TimeStampedModel
from users.models import User
from rooms.models import Room


class List(TimeStampedModel):
    """ List Model Definition """
    name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.name
