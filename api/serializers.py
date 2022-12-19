from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth import serializers as auth_serializers
from api.models import *


class RegisterCustomSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: team, part
    team = serializers.CharField()
    part = serializers.CharField()


class UserDetailCustomSerializer(auth_serializers.UserDetailsSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'team', 'part')
        read_only_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    user_team = serializers.SerializerMethodField()
    user_part = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    deleted_at = serializers.SerializerMethodField()

    class Meta:
        model = User
        # 추가 필요
        fields = ['username', 'email', 'password', 'is_active',
                  'team', 'part',
                  'created_at', 'deleted_at']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'count']

class TeamVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamVote
        fields = ['userPk', 'teamPk']