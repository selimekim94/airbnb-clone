from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel
from users.models import User
from rooms.models import Room


class Reservation(TimeStampedModel):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled')
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room} - {self.check_in}'

    def in_progress(self):
        now = timezone.now().date()
        return self.check_in <= now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
