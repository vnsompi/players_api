from rest_framework import viewsets, status
from users.models import User
from api.serializers.users import UserSerializer,RegisterSerializer
from rest_framework.response import Response



class UserViewSet(viewsets.ModelViewSet):
    """listing our users"""

    http_method_names = ['get',  'patch','delete']

    serializer_class = UserSerializer

    queryset = User.objects.all()


    """this function makes possible to get the search a users by his own uuid """
    def get_object(self):
        user = User.objects.get_object_by_public_id(self.kwargs['pk'])

        return user



class RegisterViewSet(viewsets.ViewSet):
    """Register a new user"""

    def create(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
            "user": UserSerializer(user).data
        },
            status=status.HTTP_201_CREATED,
        )
