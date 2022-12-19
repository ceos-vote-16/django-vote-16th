from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import *


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image
    Team = serializers.CharField()
    Part = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    user_team = serializers.SerializerMethodField()
    user_part = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    deleted_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        # 추가 필요
        fields = ['username', 'email', 'password', 'is_active',
                  'created_at', 'deleted_at']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'count']


class TeamVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamVote
        fields = ['userPk', 'teamPk']


class CendidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cendidate
        fields = ['name', 'count', 'part']


class CendidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CendidateVote
        fields = ['userPk', 'cendidatePk']
