from rest_framework_simplejwt.tokens import RefreshToken


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        token["username"] = user.username

        if user.escritorio:
            token["escritorio_id"] = str(user.escritorio_id)
            token["nome_escritorio"] = user.escritorio.nome

        return token
