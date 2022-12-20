from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# primary key 자동 생성
from api.utils.managers import UserManager


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()


class User(AbstractUser, BaseModel):
    email = models.EmailField(max_length=254, unique=True, verbose_name='사용자 이메일')
    password = models.CharField(max_length=128, null=False, verbose_name='사용자 비밀 번호')
    team = models.CharField(max_length=30, default='')
    part = models.CharField(max_length=10, default='')

    # customize model
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Team(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TeamVote(BaseModel):
    userPk = models.ForeignKey("User",
                               on_delete=models.CASCADE,
                               related_name="TeamVoteUserPk")
    teamPk = models.ForeignKey("Team",
                               on_delete=models.CASCADE,
                               related_name="TeamVoteTeamPk")

    def __str__(self):
        return "TeamVote"


class Candidate(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    part = models.CharField(max_length=30)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class CandidateVote(BaseModel):
    userPk = models.ForeignKey("User",
                               on_delete=models.CASCADE,
                               related_name="CandidateVoteUserPk")
    candidatePk = models.ForeignKey("Candidate",
                                    on_delete=models.CASCADE,
                                    related_name="CandidateVoteCandidatePk")

    def __str__(self):
        return "CandidateVote"
