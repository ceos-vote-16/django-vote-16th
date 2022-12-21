from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth import serializers as auth_serializers
from api.models import *
from api.utils.validator import user_register_input_validation


class RegisterCustomSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: team, part
    team = serializers.CharField()
    part = serializers.CharField()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['team'] = self.validated_data.get('team', '')
        data['part'] = self.validated_data.get('part', '')
        return data

    def validate(self, data):
        super().validate(data)
        if not user_register_input_validation(data):
            raise serializers.ValidationError("Part or Team name is invalid")
        return data


class UserDetailCustomSerializer(auth_serializers.UserDetailsSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'team', 'part')
        read_only_fields = ('username',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['name', 'count', 'part']


class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVote
        fields = ['userPk', 'candidatePk']
