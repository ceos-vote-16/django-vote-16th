from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_field

        # 기본 저장 필드: first_name, last_name, username, email
        user = super().save_user(request, user, form, False)
        # 추가 저장 필드: team,part
        user_field(user, 'team', request.data.get('team', ''))
        user_field(user, 'part', request.data.get('part', ''))
        user.save()
        return user
