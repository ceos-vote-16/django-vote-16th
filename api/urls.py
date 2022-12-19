from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

# router
# router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('votes/teams/', TeamView.as_view()),
    path('votes/cendidates/', CendidateView.as_view())
]
