from rest_framework import viewsets, status
from players.models import Player
from users.models import User
from api.serializers.users import UserSerializer,RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.decorators import action
from api.serializers.players import PlayerSerializer
from api.permissions import UserPermissions



class UserViewSet(viewsets.ModelViewSet):
    """listing our users"""
    permission_classes = [UserPermissions]

    http_method_names = ['get',  'patch','post','delete']

    serializer_class = UserSerializer

    queryset = User.objects.all()


    """this function makes possible to get the search a users by his own uuid """
    def get_object(self):
        user = User.objects.get_object_by_public_id(self.kwargs['pk'])

        """have a permissions """
        self.check_object_permissions(request = self.request, obj=user)

        return user



    """this function allow a user to add players or remove players in his favorite list """
    @action(detail=True, methods=['post'])
    def toggle_favorite(self,request, pk=None):

        player_id = request.data.get('player_id')

        user = self.get_object()
        if player_id:
            try:
               player = Player.objects.get(id=player_id)

            except Player.DoesNotExist:
                return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)

            if user.favorite_players.filter(pk=player_id).exists():
                user.favorite_players.remove(player)

                user.save()
                player_data = PlayerSerializer(player).data

                return Response({"messages": "Removed from Favorites", "player_data":player_data},
                                status=status.HTTP_200_OK)
            else:
                user.favorite_players.add(player)
                user.save()

                player_data = PlayerSerializer(player).data

                return Response({"messages": "Added from Favorites", "player_data":player_data},
                                status=status.HTTP_200_OK)

        else:
            return Response({"Error": "Please provide a valid player id"}, status=status.HTTP_400_BAD_REQUEST)


    """this function returns the list of the favorites players"""
    @action(detail=True)
    def list_favorites(self,request, pk=None):

        user = self.get_object()

        favorites = user.favorite_players.all()

        serializer = PlayerSerializer(favorites, many=True)

        return Response(serializer.data)







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


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message", 'this is a private view'}, status=status.HTTP_200_OK)


class PublicView(APIView):

    def get(self, request):
        return Response({"message", 'this is a public view'}, status=status.HTTP_200_OK)



class LoginView(viewsets.ViewSet):

    """Cette fonction authentifie un utilisateur et renvoie ses jetons JWT"""

    serializer = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        try:
           serializer.is_valid(raise_exception=True)

        except TokenError as e:
            raise InvalidToken(e)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)



