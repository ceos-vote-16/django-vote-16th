from django.urls import path, include
from rest_framework import routers

from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)

from .views import *

router = routers.DefaultRouter()

# router
router.register('users', UserViewSet)
router.register(r'votes/candidates', CandidateViewSet)
router.register('votes/teams', TeamViewSet, basename='Team-ViewSet')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('auth/login/', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('auth/logout/', LogoutCustomView.as_view(), name='rest_logout'),
    path('auth/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]

# urlpatterns = [
#     path('', include(router.urls)),
#     # path('auth/', include('dj_rest_auth.urls')),
#     path('auth/registration/', include('dj_rest_auth.registration.urls'))
# ]
