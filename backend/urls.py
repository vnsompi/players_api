
from django.contrib import admin
from django.urls import path,include
#from rest_framework_simplejwt.views import (
    #TokenObtainPairView,
    #TokenRefreshView,
#)
from api.viewsets.usersViewsets import ProtectedView,PublicView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.routes')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    path('api/public/', PublicView.as_view(), name='public_view'),

    #localhost:8000/api/
]
