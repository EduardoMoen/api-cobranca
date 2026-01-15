from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.tokens import CustomRefreshToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return CustomRefreshToken.for_user(user)
