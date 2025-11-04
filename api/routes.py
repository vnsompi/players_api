"""
routes for api
"""
from django.shortcuts import render
from rest_framework import routers
from api.viewsets.playersviewsets import PlayerListViewSet

routes = routers.SimpleRouter()
#localhost:8000/api/players


routes.register('players', PlayerListViewSet, basename='Players')

urlpatterns = routes.urls

