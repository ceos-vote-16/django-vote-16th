from django.db import models
from datetime import datetime
from django.utils import timezone
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
    email = models.EmailField(max_length=256, unique=True, verbose_name='사용자 이메일')
    password = models.CharField(max_length=128, null=False, verbose_name='사용자 비밀 번호')

    TEAM_CHOICES = [
        ("Team", "Teample"),
        ("FMN", "Forget Me Not"),
        ("PF", "Pre:Folio"),
        ("DM", "diaMEtes"),
        ("RE", "recipeasy"),
    ]
    team = models.CharField(max_length=30, choices=TEAM_CHOICES, default='')

    PART_CHOICES = [
        ("BE", "BackEnd"),
        ("FE", "FrontEnd"),
    ]
    part = models.CharField(max_length=10, choices=PART_CHOICES, default='')

    # customize model
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Team(AbstractUser, BaseModel):
    name = models.CharField(max_length=150, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TeamVote(AbstractUser, BaseModel):
    userPk = models.OneToOneField("User", on_delete=models.CASCADE)
    teamPk = models.ForeignKey("Team", on_delete=models.CASCADE)

    def __str__(self):
        return "TeamVote"
