from pydantic.functional_serializers import ModelSerializer
from rest_framework.authtoken.admin import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token