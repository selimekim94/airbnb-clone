from random import choice, randint
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from rooms.models import (Room, RoomType, Photo, Amenity, Facility, HouseRule)


class Command(BaseCommand):
    help = 'This command creates rooms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help='How many rooms you want to create'
        )

    def handle(self, *args, **options):
        number = options.get('number')
        users = User.objects.all()
        room_types = RoomType.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: choice(users),
            'room_type': lambda x: choice(room_types),
            'price': lambda x: randint(1, 300),
            'beds': lambda x: randint(1, 5),
            'bedrooms': lambda x: randint(1, 5),
            'baths': lambda x: randint(1, 5),
            'guests': lambda x: randint(1, 20),
        })
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        house_rules = HouseRule.objects.all()
        created_rooms = seeder.execute()
        created_room_ids = flatten(list(created_rooms.values()))
        for id in created_room_ids:
            room = Room.objects.get(id=id)
            for i in range(3, randint(10, 17)):
                Photo.objects.create(caption=seeder.faker.sentence(), file=f'room_photos/{randint(1, 31)}.webp',
                                     room=room)
        for amenity in amenities:
            random_number = randint(0, 15)
            if random_number % 2 == 0:
                room.amenities.add(amenity)
        for facility in facilities:
            random_number = randint(0, 15)
            if random_number % 2 == 0:
                room.facilities.add(facility)
        for house_rule in house_rules:
            random_number = randint(0, 15)
            if random_number % 2 == 0:
                room.house_rules.add(house_rule)
        self.stdout.write(self.style.SUCCESS(f'{number} rooms created!'))
