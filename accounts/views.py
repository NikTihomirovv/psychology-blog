from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer


class UserRegistrationView(CreateAPIView):
    """Регистрация нового пользователя."""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (
        AllowAny,
    )


class CurrentUserView(RetrieveAPIView):
    """Получение текущего пользователя."""

    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
    )

    def get_object(self):
        return self.request.user