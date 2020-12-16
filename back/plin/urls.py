"""plin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from trips.viewsets import TripViewSet, PlanViewSet, DayViewSet
from users.viewsets import CreateUserViewSet, MeViewSet

router = routers.DefaultRouter()
router.register(r'users', CreateUserViewSet, basename='users')
router.register(r'me', MeViewSet, basename='me')
router.register(r'trips', TripViewSet, basename='trip')

# Automatic routes for nested viewsets
trips_router = routers.NestedSimpleRouter(router, r'trips', lookup='trip')
trips_router.register(r'plans', PlanViewSet, basename='plan')
trips_router.register(r'days', DayViewSet, basename='day')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(trips_router.urls)),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')), # login to the browsable api
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
