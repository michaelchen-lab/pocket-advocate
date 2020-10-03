from rest_framework import mixins, viewsets
from rest_framework import permissions

from .serializers import ProfileSerializer
from .models import Profile

class ProfileView(
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, 
    viewsets.GenericViewSet
):
    
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return Profile.objects.filter(pk=self.request.user.id)
        #return self.request.user.profile