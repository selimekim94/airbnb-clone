from random import choice, randint
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from users.models import User
from rooms.models import Room


class Command(BaseCommand):
    help = 'This command creates reservations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='How many reservations you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(Reservation, number, {
            'status': lambda x: choice(['pending', 'confirmed', 'cancelled']),
            'guest': lambda x: choice(users),
            'room': lambda x: choice(rooms),
            'check_in': lambda x: datetime.now(),
            'check_out': lambda x: datetime.now() + timedelta(days=randint(3, 25))
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} reservations created!'))
