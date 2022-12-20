from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

# router
router.register('users', UserViewSet)
router.register(r'votes/candidates', CandidateViewSet)
router.register('votes/teams', TeamViewSet, basename='Team-ViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls'))
]
