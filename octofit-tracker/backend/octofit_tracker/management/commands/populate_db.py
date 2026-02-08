from django.core.management.base import BaseCommand
from pymongo import MongoClient
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data (direct MongoDB)'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear old data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.workouts.delete_many({})
        db.leaderboards.delete_many({})

        # Create teams
        marvel_id = db.teams.insert_one({'name': 'Marvel', 'description': 'Marvel superheroes'}).inserted_id
        dc_id = db.teams.insert_one({'name': 'DC', 'description': 'DC superheroes'}).inserted_id

        # Create users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id, 'is_active': True},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id, 'is_active': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id, 'is_active': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id, 'is_active': True},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Create activities
        activities = [
            {'user_id': user_ids[0], 'activity_type': 'Running', 'duration_minutes': 30, 'date': timezone.now().date().isoformat()},
            {'user_id': user_ids[1], 'activity_type': 'Cycling', 'duration_minutes': 45, 'date': timezone.now().date().isoformat()},
            {'user_id': user_ids[2], 'activity_type': 'Swimming', 'duration_minutes': 25, 'date': timezone.now().date().isoformat()},
            {'user_id': user_ids[3], 'activity_type': 'Yoga', 'duration_minutes': 60, 'date': timezone.now().date().isoformat()},
        ]
        db.activities.insert_many(activities)

        # Create workouts
        w1_id = db.workouts.insert_one({'name': 'Full Body Blast', 'description': 'A full body workout', 'suggested_for': user_ids[:2]}).inserted_id
        w2_id = db.workouts.insert_one({'name': 'Cardio Burn', 'description': 'High intensity cardio', 'suggested_for': user_ids[2:]}).inserted_id

        # Create leaderboards
        db.leaderboards.insert_one({'team_id': marvel_id, 'total_points': 100, 'last_updated': timezone.now()})
        db.leaderboards.insert_one({'team_id': dc_id, 'total_points': 90, 'last_updated': timezone.now()})

        # Ensure unique index on email
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with test data using direct MongoDB!'))
