from random import choice, randint
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room


class Command(BaseCommand):
    help = 'This command creates lists'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='How many lists you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(List, number, {
            'user': lambda x: choice(users)
        })
        created_lists = seeder.execute()
        created_lists_ids = flatten(list(created_lists.values()))
        for id in created_lists_ids:
            created_list = List.objects.get(id=id)
            rooms = rooms[:randint(0, len(rooms) - 1)]
            created_list.rooms.add(*rooms)
        self.stdout.write(self.style.SUCCESS(f'{number} lists created!'))
