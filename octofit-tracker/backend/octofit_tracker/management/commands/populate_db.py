from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, Activity, Leaderboard, Workout, User  # Use the custom User model
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear existing users to avoid duplicate key errors
        User.objects.all().delete()

        # Create users
        users = [
            User.objects.create(email='thundergod@mhigh.edu', name='thundergod', age=25),
            User.objects.create(email='metalgeek@mhigh.edu', name='metalgeek', age=22),
            User.objects.create(email='zerocool@mhigh.edu', name='zerocool', age=20),
            User.objects.create(email='crashoverride@mhigh.edu', name='crashoverride', age=23),
            User.objects.create(email='sleeptoken@mhigh.edu', name='sleeptoken', age=21),
        ]

        # Create teams
        teams = [
            Team.objects.create(name='Blue Team'),
            Team.objects.create(name='Gold Team')
        ]
        # Ensure correct User instances are passed to the members.add() method
        teams[0].members.add(*[user for user in users[:2]])
        teams[1].members.add(*[user for user in users[2:]])

        # Create activities
        activities = [
            Activity.objects.create(user=users[0], activity_type='Cycling', duration=60),
            Activity.objects.create(user=users[1], activity_type='Crossfit', duration=120),
            Activity.objects.create(user=users[2], activity_type='Running', duration=90),
            Activity.objects.create(user=users[3], activity_type='Strength', duration=30),
            Activity.objects.create(user=users[4], activity_type='Swimming', duration=75),
        ]

        # Update leaderboard creation logic to remove the _id field
        leaderboard_entries = [
            Leaderboard.objects.create(user=users[0], score=100),
            Leaderboard.objects.create(user=users[1], score=90),
            Leaderboard.objects.create(user=users[2], score=95),
            Leaderboard.objects.create(user=users[3], score=85),
            Leaderboard.objects.create(user=users[4], score=80),
        ]

        # Update workout creation logic to remove the _id field
        workouts = [
            Workout.objects.create(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout.objects.create(name='Crossfit', description='Training for a crossfit competition', duration=90),
            Workout.objects.create(name='Running Training', description='Training for a marathon', duration=120),
            Workout.objects.create(name='Strength Training', description='Training for strength', duration=45),
            Workout.objects.create(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
