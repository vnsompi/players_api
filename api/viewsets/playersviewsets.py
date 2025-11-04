from rest_framework import viewsets
from api.serializers.players import PlayerSerializer
from players.models import Player
from rest_framework.exceptions import ValidationError


class PlayerListViewSet(viewsets.ModelViewSet):
    """list all players"""
    http_method_names = ['get']

    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


class PlayersSearchViewSet(viewsets.ModelViewSet):
    """ search players """
    http_method_names = ['get']
    serializer_class = PlayerSerializer


    def get_queryset(self):
        queryset = Player.objects.all()

        #search by name
        name = self.request.query_params.get("name")
        #and by clubs
        club = self.request.query_params.get("club")

        min_age = self.request.query_params.get("min_age")

        max_age = self.request.query_params.get("max_age")



        if name and len(name) < 2:
            raise ValidationError({"name": " must be at least 2 characters"})

        if name:
            queryset = queryset.filter(name__contains=name)

        if club:
            queryset = queryset.filter(club=club)

        if min_age and max_age:
            queryset = queryset.filter(age__range=(min_age, max_age))

        return queryset



