
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tokens', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/', include('core.urls')),
    path('creators/', include('creator.urls')),
    path('youtube/', include('catalog.urls')),
]
