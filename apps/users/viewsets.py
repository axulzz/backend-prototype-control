from rest_framework.viewsets import mixins, GenericViewSet
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()

    serializer_class = UserListSerializer

    def get_queryset(self):
        return self.queryset
