import os
import django
import sys
from pathlib import Path

# Ensure the backend directory is in the PYTHONPATH
backend_path = Path(__file__).resolve().parent.parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))  # Use insert(0) to prioritize this path

# Add the project root directory to sys.path to resolve imports
project_root = backend_path.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add the octofit_tracker directory to sys.path to resolve imports
octofit_tracker_path = backend_path / 'octofit_tracker'
if str(octofit_tracker_path) not in sys.path:
    sys.path.append(str(octofit_tracker_path))  # Use append to avoid conflicts

# Ensure the Django settings module is set before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, Activity, Leaderboard, Workout, User  # Use the custom User model
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta, date
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            # Connect to MongoDB
            mongo_host = settings.MONGO_DATABASES['HOST']
            mongo_port = settings.MONGO_DATABASES['PORT']
            mongo_name = settings.MONGO_DATABASES['NAME']
            client = MongoClient(mongo_host, mongo_port)
            db = client[mongo_name]

            # Drop existing collections
            db.users.drop()
            db.teams.drop()
            db.activities.drop()
            db.leaderboard.drop()
            db.workouts.drop()

            # Clear existing users to avoid duplicate key errors
            User.objects.all().delete()

            # Create users with passwords
            users = [
                User.objects.create_user(email='thundergod@mhigh.edu', name='thundergod', age=25, password='password123'),
                User.objects.create_user(email='metalgeek@mhigh.edu', name='metalgeek', age=22, password='password123'),
                User.objects.create_user(email='zerocool@mhigh.edu', name='zerocool', age=20, password='password123'),
                User.objects.create_user(email='crashoverride@mhigh.edu', name='crashoverride', age=23, password='password123'),
                User.objects.create_user(email='sleeptoken@mhigh.edu', name='sleeptoken', age=21, password='password123'),
            ]

            # Create teams
            teams = [
                Team.objects.create(name='Blue Team'),
                Team.objects.create(name='Gold Team')
            ]
            teams[0].members.add(*[user for user in users[:2]])
            teams[1].members.add(*[user for user in users[2:]])

            # Create activities
            activities = [
                Activity.objects.create(user=users[0], activity_type='Cycling', duration=60, date=date(2025, 4, 1)),
                Activity.objects.create(user=users[1], activity_type='Crossfit', duration=120, date=date(2025, 4, 2)),
                Activity.objects.create(user=users[2], activity_type='Running', duration=90, date=date(2025, 4, 3)),
                Activity.objects.create(user=users[3], activity_type='Strength', duration=30, date=date(2025, 4, 4)),
                Activity.objects.create(user=users[4], activity_type='Swimming', duration=75, date=date(2025, 4, 5)),
            ]

            # Create leaderboard entries
            leaderboard_entries = [
                Leaderboard.objects.create(user=users[0], score=100),
                Leaderboard.objects.create(user=users[1], score=90),
                Leaderboard.objects.create(user=users[2], score=95),
                Leaderboard.objects.create(user=users[3], score=85),
                Leaderboard.objects.create(user=users[4], score=80),
            ]

            # Create workouts
            workouts = [
                Workout.objects.create(name='Cycling Training', description='Training for a road cycling event', duration=60),
                Workout.objects.create(name='Crossfit', description='Training for a crossfit competition', duration=90),
                Workout.objects.create(name='Running Training', description='Training for a marathon', duration=120),
                Workout.objects.create(name='Strength Training', description='Training for strength', duration=45),
                Workout.objects.create(name='Swimming Training', description='Training for a swimming competition', duration=75),
            ]

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error populating the database: {e}'))
        finally:
            if 'client' in locals():
                client.close()
