"""
routes for api
"""
from django.shortcuts import render
from rest_framework import routers
from api.viewsets.playersviewsets import PlayerListViewSet,PlayersSearchViewSet
from api.viewsets.usersViewsets import UserViewSet, RegisterViewSet

routes = routers.SimpleRouter()
#localhost:8000/api/players


routes.register('players', PlayerListViewSet, basename='Players')
routes.register('search', PlayersSearchViewSet, basename='Search_Player')
routes.register('users', UserViewSet, basename='Users')
routes.register('auth/register', RegisterViewSet, basename='Register')

urlpatterns = routes.urls

