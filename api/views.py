from dj_rest_auth.views import LogoutView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

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


class LogoutCustomView(APIView):
    def post(self, request, *args, **kwargs):
        return self.logoutCustom(request)

    def logoutCustom(self, request):
        from django.contrib.auth import logout as django_logout
        from django.utils.translation import gettext_lazy as _

        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response(
            {'detail': _('Successfully logged out.')},
            status=status.HTTP_200_OK,
        )
        # if getattr(settings, 'REST_USE_JWT', False):
        #
        #     # NOTE: this import occurs here rather than at the top level
        #     # because JWT support is optional, and if `REST_USE_JWT` isn't
        #     # True we shouldn't need the dependency
        #     from rest_framework_simplejwt.exceptions import TokenError
        #     from rest_framework_simplejwt.tokens import RefreshToken
        #
        #     from .jwt_auth import unset_jwt_cookies
        #     cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
        #
        #     unset_jwt_cookies(response)
        #
        #     if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        #         # add refresh token to blacklist
        #         try:
        #             token = RefreshToken(request.data['refresh'])
        #             token.blacklist()
        #         except KeyError:
        #             response.data = {'detail': _('Refresh token was not included in request data.')}
        #             response.status_code =status.HTTP_401_UNAUTHORIZED
        #         except (TokenError, AttributeError, TypeError) as error:
        #             if hasattr(error, 'args'):
        #                 if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
        #                     response.data = {'detail': _(error.args[0])}
        #                     response.status_code = status.HTTP_401_UNAUTHORIZED
        #                 else:
        #                     response.data = {'detail': _('An error has occurred.')}
        #                     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        #
        #             else:
        #                 response.data = {'detail': _('An error has occurred.')}
        #                 response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        #
        #     elif not cookie_name:
        #         message = _(
        #             'Neither cookies or blacklist are enabled, so the token '
        #             'has not been deleted server side. Please make sure the token is deleted client side.',
        #         )
        #         response.data = {'detail': message}
        #         response.status_code = status.HTTP_200_OK
        return response
