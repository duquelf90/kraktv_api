from django.shortcuts import render

from rest_framework import generics
from .models import SocialLink
from .serializers import CreatorSerializer, SocialLinkSerializer, SocialLinkListSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SocialLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialLink.objects.filter(creator=self.request.user)


class SocialLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialLink.objects.filter(creator=self.request.user)
   
    
class SocialLinkBulkUpdateView(generics.UpdateAPIView):
    serializer_class = SocialLinkListSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Iterar sobre los enlaces y actualizar o crear según sea necesario
        for link_data in serializer.validated_data['links']:
            link_id = link_data.get('id')
            if link_id:
                # Actualizar el enlace existente
                SocialLink.objects.filter(id=link_id, creator=request.user).update(
                    platform=link_data['platform'],
                    url=link_data['url'],
                    order=link_data['order']
                )
            else:
                # Crear un nuevo enlace
                SocialLink.objects.create(
                    platform=link_data['platform'],
                    url=link_data['url'],
                    order=link_data['order'],
                    creator=request.user
                )

        return Response({'message': 'Enlaces actualizados correctamente.'})
    
class CreatorDetailView(generics.RetrieveAPIView):
    serializer_class = CreatorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user