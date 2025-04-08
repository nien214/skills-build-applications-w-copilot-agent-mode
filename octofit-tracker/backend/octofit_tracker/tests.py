from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(email="test@example.com", name="Test User", age=25)
        self.assertEqual(user.email, "test@example.com")

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(email="test@example.com", name="Test User", age=25)
        team = Team.objects.create(name="Test Team")
        team.members.add(user)
        self.assertEqual(team.name, "Test Team")

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create(email="test@example.com", name="Test User", age=25)
        activity = Activity.objects.create(user=user, activity_type="Running", duration=30, date="2025-04-08")
        self.assertEqual(activity.activity_type, "Running")

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        user = User.objects.create(email="test@example.com", name="Test User", age=25)
        leaderboard = Leaderboard.objects.create(user=user, score=100)
        self.assertEqual(leaderboard.score, 100)

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name="Morning Yoga", description="A relaxing yoga session", duration=60)
        self.assertEqual(workout.name, "Morning Yoga")

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        # Define the payload for registration
        payload = {
            "email": "testuser@example.com",
            "name": "Test User",
            "age": 25
        }

        # Make a POST request to the /api/users/ endpoint
        response = self.client.post("/api/users/", payload)

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the user was created in the database
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_duplicate_email_registration(self):
        # Create an initial user
        User.objects.create(email="testuser@example.com", name="Test User", age=25)

        # Attempt to register with the same email
        payload = {
            "email": "testuser@example.com",
            "name": "Another User",
            "age": 30
        }
        response = self.client.post("/api/users/", payload)

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the error message indicates a duplicate email
        self.assertIn("email", response.data)
