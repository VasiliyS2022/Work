from urllib import request, response
from rest_framework import viewsets
from album.api.v1 import serializers
from album.models import Album


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = serializers.AlbumSerializer

    def filter_queryset(self, queryset):
        queryset = super(AlbumViewSet, self).filter_queryset(queryset)
        sorting = self.request.query_params.get("sorting")
        if sorting:
            queryset = queryset.order_by(f"-{sorting}")

        return queryset