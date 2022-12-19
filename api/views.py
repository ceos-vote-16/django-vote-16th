from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
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

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # filterset_class = TeamFilter
    ordering_fields = ['count', 'name']
    ordering = ['name']

    lookup_body_field = 'name'

    def put(self, pk=None):
        lookup_value = self.request.data.get(self.lookup_body_field)
        if not lookup_value:
            raise ValidationError({self.lookup_body_field: "This field is mandatory"})

        obj = self.get_queryset().filter(**{self.lookup_body_field: lookup_value}).last()
        if not obj:
            return self.create(request=self.request)
        else:
            self.kwargs['pk'] = obj.pk

            self.request.data._mutable = True
            self.request.data['count'] = obj.count+1
            self.request.data._mutable = False

            return self.update(request=self.request)


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
