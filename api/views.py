from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from api.utils.common import custom_response, CustomRenderer
from api.utils.permission import IsAuthenticatedInPutReq
from api.serializers import *
from api.utils.filters import *
from api.utils.validator import candidate_put_input_validation, team_put_input_validation


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = UserFilter
    ordering_fields = ['name', 'team', 'part']

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.delete()
        user.save()
        return Response(data='delete user success')


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticatedInPutReq]
    renderer_classes = [CustomRenderer]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['count', 'name']
    ordering = ['name']

    lookup_body_field = 'name'

    def update(self, request, *args, **kwargs):
        self.put(self)

    def put(self, pk=None):
        try:
            lookup_value = self.request.data
            if not team_put_input_validation(lookup_value):
                return JsonResponse(custom_response(400), status=400)

            team = self.get_queryset().filter(
                **{self.lookup_body_field: lookup_value.get(self.lookup_body_field)}).last()
            if not team:
                return JsonResponse(custom_response(404), status=404)
            else:
                user = self.request.user
                team.count = team.count + 1
                team.save()
                team_vote_serializer = TeamVoteSerializer(data={
                    'userPk': user.id,
                    'teamPk': team.id
                })
                if team_vote_serializer.is_valid():
                    team_vote_serializer.save()
                    return JsonResponse(custom_response(200), status=200)
                return JsonResponse(custom_response(404), status=404)
        except:
            return JsonResponse(custom_response(404), status=404)


class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()
    permission_classes = [IsAuthenticatedInPutReq]
    renderer_classes = [CustomRenderer]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = CandidateFilter
    ordering_fields = ['count', 'name']
    ordering = ['name']

    def update(self, request, *args, **kwargs):
        self.put(self)

    def put(self, pk=None):
        try:
            lookup_value = self.request.data
            if not candidate_put_input_validation(lookup_value):
                return JsonResponse(custom_response(400), status=400)

            name, part = lookup_value.get("name"), lookup_value.get("part")
            candidate = self.get_queryset().get(name=name, part=part)
            if not candidate:
                return JsonResponse(custom_response(404), status=404)
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
        except:
            return JsonResponse(custom_response(404), status=404)
