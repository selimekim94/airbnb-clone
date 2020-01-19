from django.db import models
from core.models import TimeStampedModel
from users.models import User


class Conversation(TimeStampedModel):
    """ Conversation Model Definition """
    participants = models.ManyToManyField(User, related_name='conversations', blank=True)

    def __str__(self):
        return str(self.created_at)


class Message(TimeStampedModel):
    """ Message Model Definition """
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return self.message
