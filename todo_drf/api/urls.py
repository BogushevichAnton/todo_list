from django.urls import path, include
from .views import NotesViewSet, CategoryViewSet
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'notes', NotesViewSet)
router.register(r'categories', CategoryViewSet)
#router.register(r'user', UserViewSet)

urlpatterns = [
    # ex: /polls/
    path("", include((router.urls, 'api-v1'), namespace='instance_name')),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
]