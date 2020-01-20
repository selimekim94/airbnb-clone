from django.db import models
from core.models import TimeStampedModel
from users.models import User


class Conversation(TimeStampedModel):
    """ Conversation Model Definition """
    participants = models.ManyToManyField(User, related_name='conversations', blank=True)

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return f'[{", ".join(usernames)}]'

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = 'Number of Messages'

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = 'Number of Participants'


class Message(TimeStampedModel):
    """ Message Model Definition """
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} says: {self.message}'
