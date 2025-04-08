from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Octofit API!",
        "url": "https://literate-lamp-97w767q6wp46279q9-8000.app.github.dev"
    })

@api_view(['GET'])
def personalized_workouts(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)

    # Example logic for personalized suggestions
    suggestions = [
        {'name': 'Morning Yoga', 'duration': '30 mins', 'calories': 150},
        {'name': 'Evening Run', 'duration': '45 mins', 'calories': 400},
    ]

    return Response({'workout_suggestions': suggestions})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
