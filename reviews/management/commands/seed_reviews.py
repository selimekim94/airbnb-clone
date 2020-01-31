from random import choice, randint
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users.models import User
from rooms.models import Room


class Command(BaseCommand):
    help = 'This command creates reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='How many reviews you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(Review, number, {
            'accuracy': lambda x: randint(0, 5),
            'communication': lambda x: randint(0, 5),
            'cleanliness': lambda x: randint(0, 5),
            'location': lambda x: randint(0, 5),
            'check_in': lambda x: randint(0, 5),
            'value': lambda x: randint(0, 5),
            'user': choice(users),
            'room': choice(rooms)
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} reviews created!'))
