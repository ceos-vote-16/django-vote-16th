from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from api.common import custom_response
from api.serializers import *
from api.utils.filters import *


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = UserFilter

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.delete()
        user.save()
        return Response(data='delete user success')


class TeamView(APIView):
    def get(self, request):
        try:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
            return JsonResponse(custom_response(200, serializer.data), status=200)
        except:
            return JsonResponse(custom_response(401), status=401)

    def post(self, request):
        # team valid check
        team_name = request.data.get("team_name")
        chosen_team = Team.objects.get(name=team_name)
        if chosen_team is None:
            return JsonResponse(custom_response(400), status=400)

        # user valid check
        user_name = request.data.get("user_name")
        chosen_user = User.objects.get(username=user_name)
        if chosen_user is None:
            return JsonResponse(custom_response(400), status=400)

        chosen_team.count = chosen_team.count + 1
        chosen_team.save()
        team_vote_serializer = TeamVoteSerializer(data={
            'userPk': chosen_user.id,
            'teamPk': chosen_team.id
        })
        if team_vote_serializer.is_valid():
            team_vote_serializer.save()
            return JsonResponse(custom_response(200), status=200)
        return JsonResponse(custom_response(404), status=404)


class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['count', 'name']
    ordering = ['name']

    frontend_condition = ["FE", "Frontend"]
    backend_condition = ["BE", "Backend"]

    def get_queryset(self):
        queryset = super().get_queryset()
        lookup_part = self.request.query_params.get("part")
        if lookup_part == "FE" or lookup_part == "Frontend":
            queryset = queryset.filter(part__in=self.frontend_condition)
        elif lookup_part == "BE" or lookup_part == "Backend":
            queryset = queryset.filter(part__in=self.backend_condition)
        return queryset

    def put(self, pk=None):
        lookup_value = self.request.data
        if not lookup_value:
            raise ValidationError("This field is mandatory")

        candidate = self.get_queryset().get(**lookup_value)
        if not candidate:
            raise ValidationError("There's no such candidate")
        else:
            user = self.request.user
            candidate.count = candidate.count + 1
            candidate.save()
            candidate_vote_serializer = CandidateVoteSerializer(data={
                'userPk': user.id,
                'candidatePk': candidate.id
            })
            if candidate_vote_serializer.is_valid():
                candidate_vote_serializer.save()
                return JsonResponse(custom_response(200), status=200)
            return JsonResponse(custom_response(404), status=404)